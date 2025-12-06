package userRepository

import (
	"context"
	"fmt"
	"visitor-management/internal/domain"

	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

type VisitorRepo struct {
	db        *dynamodb.Client
	tableName string
}

func NewVisitorRepo(db *dynamodb.Client, tableName string) *VisitorRepo {
	return &VisitorRepo{db: db, tableName: tableName}
}

// CREATE VISITOR
func (r *VisitorRepo) Create(v *domain.Visitor) error {

	query := fmt.Sprintf(`
	INSERT INTO "%s" VALUE {
		'PK' : 'VISITORS',
		'SK' : 'VISITOR#%s#%s',
		'ID' : '%s',
		'Name' : '%s',
		'Email' : '%s',
		'Tower' : '%s',
		'FlatNo' : '%s',
		'AddedByRole' : '%s',
		'Status' : '%s',
		'OwnerEmail' : '%s',
		'OwnerID' : '%s',
		'CreatedAt' : %d
	}	
	`, r.tableName, v.OwnerID, v.ID, v.ID, v.Name, v.Email, v.Tower, v.FlatNo, v.AddedByRole,
		v.Status, v.OwnerEmail, v.OwnerID, v.CreatedAt)

	_, err := r.db.ExecuteStatement(context.TODO(), &dynamodb.ExecuteStatementInput{
		Statement: &query,
	})
	return err
}

func (r *VisitorRepo) GetAllVisitors() ([]domain.Visitor, error) {

	query := fmt.Sprintf(`
	SELECT * FROM "%s" WHERE PK='VISITORS' AND begins_with(SK, 'VISITOR#')
	`, r.tableName)

	out, err := r.db.ExecuteStatement(context.TODO(), &dynamodb.ExecuteStatementInput{
		Statement: &query,
	})
	if err != nil {
		return nil, err
	}

	var visitors []domain.Visitor
	attributevalue.UnmarshalListOfMaps(out.Items, &visitors)

	return visitors, nil
}


func (r *VisitorRepo) GetVisitorsByOwner(ownerID string) ([]domain.Visitor, error) {

	query := fmt.Sprintf(`
	SELECT * FROM "%s" 
	WHERE PK='VISITORS' AND begins_with(SK, 'VISITOR#%s')
	`, r.tableName, ownerID)

	out, err := r.db.ExecuteStatement(context.TODO(), &dynamodb.ExecuteStatementInput{
		Statement: &query,
	})
	if err != nil {
		return nil, err
	}

	var visitors []domain.Visitor
	attributevalue.UnmarshalListOfMaps(out.Items, &visitors)

	return visitors, nil
}


func (r *VisitorRepo) CountVisitors() (int, error) {
	visitors, err := r.GetAllVisitors()
	if err != nil {
		return 0, err
	}
	return len(visitors), nil
}


func (r *VisitorRepo) UpdateVisitorStatus(visitorID, ownerID, status string) error {

	query := fmt.Sprintf(`
	UPDATE "%s" 
	SET Status='%s'
	WHERE PK='VISITORS' AND SK='VISITOR#%s#%s'
	`, r.tableName, status, ownerID, visitorID)

	_, err := r.db.ExecuteStatement(context.TODO(), &dynamodb.ExecuteStatementInput{
		Statement: &query,
	})
	return err
}
