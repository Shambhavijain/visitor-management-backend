package userRepository

import (
	"context"
	"fmt"
	"log"
	"visitor-management/internal/domain"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
	"golang.org/x/crypto/bcrypt"
)

type UserRepo struct {
	db        *dynamodb.Client
	tableName string
}

func NewUserRepo(db *dynamodb.Client, tableName string) *UserRepo {
	return &UserRepo{db: db, tableName: tableName}
}

func (r *UserRepo) GetByEmail(email string) (*domain.User, error) {

	log.Printf("Received login request for email: %s", email)

	statement := fmt.Sprintf(
		"SELECT * FROM %s WHERE PK = ? AND SK = ?",
		r.tableName,
	)

	params := []types.AttributeValue{
		&types.AttributeValueMemberS{Value: "USERS"},
		&types.AttributeValueMemberS{Value: "EMAIL#" + email},
	}

	log.Printf("Executing query: %s with params: %v", statement, params)

	result, err := r.db.ExecuteStatement(context.Background(), &dynamodb.ExecuteStatementInput{
		Statement:  aws.String(statement),
		Parameters: params,
	})
	log.Printf("result %+v", result)

	if err != nil {
		log.Print(err.Error())
		return nil, fmt.Errorf("failed to query user: %w", err)
	}

	if len(result.Items) == 0 {
		log.Printf("No user found for email: %s", email)
		return nil, fmt.Errorf("user not found for email: %s", email)
	}

	var user domain.User
	err = attributevalue.UnmarshalMap(result.Items[0], &user)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal user: %w", err)
	}

	log.Printf("User found: %+v", user)

	return r.GetUserById(user.ID)
}

func (r *UserRepo) Create(user domain.User) error {
	log.Printf("Creating user: %+v", user)

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		return fmt.Errorf("failed to hash password: %w", err)
	}

	statement := fmt.Sprintf(
		"INSERT INTO %s VALUE {'PK': ?, 'SK': ?, 'UserId': ?, 'Username': ?, 'Password': ?, 'Role': ?, 'Email': ?, 'Address': ?, 'Flat_no': ?, 'Tower': ?}",
		r.tableName,
	)
	log.Printf("PartiQL statement: %s", statement)

	userParams := []types.AttributeValue{
		&types.AttributeValueMemberS{Value: "USERS"},
		&types.AttributeValueMemberS{Value: "Users#" + user.ID},
		&types.AttributeValueMemberS{Value: user.ID},
		&types.AttributeValueMemberS{Value: user.Username},
		&types.AttributeValueMemberS{Value: string(hashedPassword)},
		&types.AttributeValueMemberS{Value: user.Role},
		&types.AttributeValueMemberS{Value: user.Email},
		&types.AttributeValueMemberS{Value: user.Address},
		&types.AttributeValueMemberS{Value: user.FlatNo},
		&types.AttributeValueMemberS{Value: user.Tower},
	}

	emailParams := []types.AttributeValue{
		&types.AttributeValueMemberS{Value: "USERS"},
		&types.AttributeValueMemberS{Value: "EMAIL#" + user.Email},
		&types.AttributeValueMemberS{Value: user.ID},
		&types.AttributeValueMemberS{Value: user.Username},
		&types.AttributeValueMemberS{Value: string(hashedPassword)},
		&types.AttributeValueMemberS{Value: user.Role},
		&types.AttributeValueMemberS{Value: user.Email},
		&types.AttributeValueMemberS{Value: user.Address},
		&types.AttributeValueMemberS{Value: ""},
		&types.AttributeValueMemberS{Value: ""},
	}

	towerParams := []types.AttributeValue{
		&types.AttributeValueMemberS{Value: "USERS"},
		&types.AttributeValueMemberS{Value: fmt.Sprintf("Tower#%s#Flat_no#%s", user.Tower, user.FlatNo)},
		&types.AttributeValueMemberS{Value: user.ID},
		&types.AttributeValueMemberS{Value: user.Username},
		&types.AttributeValueMemberS{Value: string(hashedPassword)},
		&types.AttributeValueMemberS{Value: ""},
		&types.AttributeValueMemberS{Value: user.Email},
		&types.AttributeValueMemberS{Value: ""},
		&types.AttributeValueMemberS{Value: user.FlatNo},
		&types.AttributeValueMemberS{Value: user.Tower},
	}

	transact := &dynamodb.ExecuteTransactionInput{
		TransactStatements: []types.ParameterizedStatement{
			{Statement: aws.String(statement), Parameters: userParams},
			{Statement: aws.String(statement), Parameters: emailParams},
			{Statement: aws.String(statement), Parameters: towerParams},
		},
	}

	_, err = r.db.ExecuteTransaction(context.TODO(), transact)
	if err != nil {
		return fmt.Errorf("transaction failed: %w", err)
	}

	log.Printf("ERROR in Create(): %v", err)
	log.Printf("User %s created successfully", user.Email)
	return nil
}

func (r *UserRepo) UpdateUser(user domain.User) error {

	return nil
}

func (r *UserRepo) Delete(userID string) error {

	statementUserQuery := fmt.Sprintf(
		"SELECT Email, Tower, Flat_no FROM %s WHERE PK=? AND SK=?",
		r.tableName,
	)

	getResult, err := r.db.ExecuteStatement(context.Background(),
		&dynamodb.ExecuteStatementInput{
			Statement: aws.String(statementUserQuery),
			Parameters: []types.AttributeValue{
				&types.AttributeValueMemberS{Value: "USERS"},
				&types.AttributeValueMemberS{Value: "Users#" + userID},
			},
		},
	)
	if err != nil {
		return fmt.Errorf("failed to fetch user before delete: %w", err)
	}

	if len(getResult.Items) == 0 {
		return fmt.Errorf("user not found: %s", userID)
	}

	var userItem struct {
		Email  string `dynamodbav:"Email"`
		Tower  string `dynamodbav:"Tower"`
		FlatNo string `dynamodbav:"Flat_no"`
	}

	if err := attributevalue.UnmarshalMap(getResult.Items[0], &userItem); err != nil {
		return fmt.Errorf("failed to unmarshal fetched user: %w", err)
	}
	log.Printf("%+v", userItem)
	email := userItem.Email
	tower := userItem.Tower
	flatNo := userItem.FlatNo

	deleteStmt := fmt.Sprintf("DELETE FROM %s WHERE PK=? AND SK=?", r.tableName)

	input := &dynamodb.ExecuteTransactionInput{
		TransactStatements: []types.ParameterizedStatement{

			{
				Statement: aws.String(deleteStmt),
				Parameters: []types.AttributeValue{
					&types.AttributeValueMemberS{Value: "USERS"},
					&types.AttributeValueMemberS{Value: "EMAIL#" + email},
				},
			},

			{
				Statement: aws.String(deleteStmt),
				Parameters: []types.AttributeValue{
					&types.AttributeValueMemberS{Value: "USERS"},
					&types.AttributeValueMemberS{Value: "Users#" + userID},
				},
			},

			{
				Statement: aws.String(deleteStmt),
				Parameters: []types.AttributeValue{
					&types.AttributeValueMemberS{Value: "USERS"},
					&types.AttributeValueMemberS{Value: fmt.Sprintf("Tower#%s#Flat_no#%s", tower, flatNo)},
				},
			},
		},
	}

	_, err = r.db.ExecuteTransaction(context.Background(), input)
	if err != nil {
		return fmt.Errorf("transaction delete failed: %w", err)
	}

	return nil
}

func (r *UserRepo) GetallUsers() ([]domain.User, error) {

	statement := fmt.Sprintf(
		"SELECT * FROM %s WHERE PK = ? AND begins_with(SK, ?)",
		r.tableName,
	)

	result, err := r.db.ExecuteStatement(context.Background(), &dynamodb.ExecuteStatementInput{
		Statement: aws.String(statement),
		Parameters: []types.AttributeValue{
			&types.AttributeValueMemberS{Value: "USERS"},
			&types.AttributeValueMemberS{Value: "Users#"},
		},
	})

	if err != nil {
		return nil, fmt.Errorf("failed to get users: %w", err)
	}

	var users []domain.User
	for _, item := range result.Items {
		var user domain.User
		err = attributevalue.UnmarshalMap(item, &user)
		if err != nil {
			continue
		}
		users = append(users, user)
	}

	return users, nil
}

func (r *UserRepo) GetUserById(userID string) (*domain.User, error) {

	statement := fmt.Sprintf("SELECT * FROM %s WHERE PK = ? AND SK = ?", r.tableName)

	result, err := r.db.ExecuteStatement(context.Background(), &dynamodb.ExecuteStatementInput{
		Statement: aws.String(statement),
		Parameters: []types.AttributeValue{
			&types.AttributeValueMemberS{Value: "USERS"},
			&types.AttributeValueMemberS{Value: "Users#" + userID},
		},
	})

	if err != nil {
		return nil, err
	}
	log.Print(err)

	if len(result.Items) == 0 {
		return nil, fmt.Errorf("user not found")
	}

	var user domain.User
	err = attributevalue.UnmarshalMap(result.Items[0], &user)
	if err != nil {
		return nil, err
	}
	log.Print(user)
	return &user, nil
}

func (r *UserRepo) GetOwnerByTowerAndFlat(tower string, flatNo string) (*domain.User, error) {

	statement := fmt.Sprintf(
		"SELECT * FROM %s WHERE PK = ? AND SK = ?",
		r.tableName,
	)

	result, err := r.db.ExecuteStatement(context.Background(), &dynamodb.ExecuteStatementInput{
		Statement: aws.String(statement),
		Parameters: []types.AttributeValue{
			&types.AttributeValueMemberS{Value: "USERS"},
			&types.AttributeValueMemberS{Value: "Tower#" + tower + "#Flat_no#" + flatNo},
		},
	})

	if err != nil {
		return nil, fmt.Errorf("failed to get owner by tower and flat: %w", err)
	}

	if len(result.Items) == 0 {
		return nil, fmt.Errorf("owner not found for tower %s and flat %s", tower, flatNo)
	}

	var user domain.User
	err = attributevalue.UnmarshalMap(result.Items[0], &user)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal user: %w", err)
	}

	return &user, nil
}

func (r *UserRepo) GetUsersCount() (domain.UsersCount, error) {
	log.Println("[GetUsersCount] Starting count...")

	owners, err := r.countRole("owner")
	if err != nil {
		log.Printf("[GetUsersCount] Owner count failed: %v\n", err)
		return domain.UsersCount{}, fmt.Errorf("count owner failed: %w", err)
	}

	gatekeepers, err := r.countRole("gatekeeper")
	if err != nil {
		log.Printf("[GetUsersCount] Gatekeeper count failed: %v\n", err)
		return domain.UsersCount{}, fmt.Errorf("count gatekeeper failed: %w", err)
	}

	log.Printf("[GetUsersCount] Result → Owners: %d, Gatekeepers: %d\n", owners, gatekeepers)

	return domain.UsersCount{
		Owner:      owners,
		Gatekeeper: gatekeepers,
	}, nil
}

func (r *UserRepo) countRole(role string) (int, error) {

	stmt := fmt.Sprintf(
		"SELECT * FROM %s WHERE PK = ? AND begins_with(SK, ?) AND Role = ?",
		r.tableName,
	)

	log.Printf("[countRole:%s] PartiQL: %s\n", role, stmt)

	params := []types.AttributeValue{
		&types.AttributeValueMemberS{Value: "USERS"},
		&types.AttributeValueMemberS{Value: "Users#"},
		&types.AttributeValueMemberS{Value: role},
	}

	res, err := r.db.ExecuteStatement(
		context.Background(),
		&dynamodb.ExecuteStatementInput{
			Statement:  aws.String(stmt),
			Parameters: params,
		})
	if err != nil {
		return 0, fmt.Errorf("failed to count %s: %w", role, err)
	}

	return len(res.Items), nil
}
func (r *UserRepo) CreateGatekeeper(user domain.User) error {
	log.Printf("Creating user: %+v", user)

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)
	if err != nil {
		return fmt.Errorf("failed to hash password: %w", err)
	}

	statement := fmt.Sprintf(
		"INSERT INTO %s VALUE {'PK': ?, 'SK': ?, 'UserId': ?, 'Username': ?, 'Password': ?, 'Role': ?, 'Email': ?, 'Address': ?, 'Flat_no': ?, 'Tower': ?}",
		r.tableName,
	)
	log.Printf("PartiQL statement: %s", statement)

	userParams := []types.AttributeValue{
		&types.AttributeValueMemberS{Value: "USERS"},
		&types.AttributeValueMemberS{Value: "Users#" + user.ID},
		&types.AttributeValueMemberS{Value: user.ID},
		&types.AttributeValueMemberS{Value: user.Username},
		&types.AttributeValueMemberS{Value: string(hashedPassword)},
		&types.AttributeValueMemberS{Value: user.Role},
		&types.AttributeValueMemberS{Value: user.Email},
		&types.AttributeValueMemberS{Value: user.Address},
		&types.AttributeValueMemberS{Value: user.FlatNo},
		&types.AttributeValueMemberS{Value: user.Tower},
	}

	emailParams := []types.AttributeValue{
		&types.AttributeValueMemberS{Value: "USERS"},
		&types.AttributeValueMemberS{Value: "EMAIL#" + user.Email},
		&types.AttributeValueMemberS{Value: user.ID},
		&types.AttributeValueMemberS{Value: user.Username},
		&types.AttributeValueMemberS{Value: string(hashedPassword)},
		&types.AttributeValueMemberS{Value: user.Role},
		&types.AttributeValueMemberS{Value: user.Email},
		&types.AttributeValueMemberS{Value: user.Address},
		&types.AttributeValueMemberS{Value: ""},
		&types.AttributeValueMemberS{Value: ""},
	}

	transact := &dynamodb.ExecuteTransactionInput{
		TransactStatements: []types.ParameterizedStatement{
			{Statement: aws.String(statement), Parameters: userParams},
			{Statement: aws.String(statement), Parameters: emailParams},
		},
	}

	_, err = r.db.ExecuteTransaction(context.TODO(), transact)
	if err != nil {
		return fmt.Errorf("transaction failed: %w", err)
	}

	log.Printf("ERROR in Create(): %v", err)
	log.Printf("User %s created successfully", user.Email)
	return nil
}