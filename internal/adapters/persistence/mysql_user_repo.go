package persistence

import (
	"database/sql"
	"fmt"
	"strings"
	"visitor-management/internal/domain"
)

type MySQLUserRepo struct {
	DB *sql.DB
}

func NewMySQLUserRepo(db *sql.DB) *MySQLUserRepo {
	return &MySQLUserRepo{DB: db}
}

func (r *MySQLUserRepo) GetByEmail(email string) (*domain.User, error) {
	email = strings.TrimSpace(email)
	query := `
SELECT id, username, role, email, password, address,
       COALESCE(flat_no, '') AS flat_no,
       COALESCE(tower, '') AS tower
FROM users
WHERE email = ?`

	row := r.DB.QueryRow(query, email)

	var user domain.User
	err := row.Scan(&user.ID, &user.Username, &user.Role, &user.Email, &user.Password, &user.Address, &user.FlatNo, &user.Tower)

	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("user not found")
	}

	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *MySQLUserRepo) Create(user domain.User) error {
	fmt.Println("Reached repo to create user")

	query := `INSERT INTO users (id, username, role, email, password, address, flat_no, tower) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
	_, err := r.DB.Exec(query, user.ID, user.Username, user.Role, user.Email, user.Password, user.Address, user.FlatNo, user.Tower)
	return err
}

func (r *MySQLUserRepo) UpdateUser(user domain.User) error {
	query := "UPDATE users SET email = ?, username = ? WHERE id = ?"
	_, err := r.DB.Exec(query, user.Email, user.Username, user.ID)
	return err
}

func (r *MySQLUserRepo) Delete(username string) error {
	fmt.Println("User Delete from Repo")
	query := `DELETE FROM users WHERE username = ?`
	_, err := r.DB.Exec(query, username)
	return err
}
func (r *MySQLUserRepo) GetallUsers() ([]domain.User, error) {

	query := `SELECT id, username, role, email, address, flat_no, tower FROM users WHERE role = 'owner'`
	rows, err := r.DB.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var users []domain.User
	for rows.Next() {
		var user domain.User
		err := rows.Scan(&user.ID, &user.Username, &user.Role, &user.Email, &user.Address, &user.FlatNo, &user.Tower)
		if err != nil {
			return nil, err
		}
		users = append(users, user)
	}

	return users, nil
}

func (r *MySQLUserRepo) GetUserById(userID string) (*domain.User, error) {

	query := `
        SELECT id, email, role, username,
               COALESCE(tower, '') AS tower,
               COALESCE(flat_no, '') AS flat_no
        FROM users
        WHERE id = ?
    `

	row := r.DB.QueryRow(query, userID)

	var user domain.User
	err := row.Scan(&user.ID, &user.Email, &user.Role, &user.Username, &user.Tower, &user.FlatNo)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}
	return &user, nil
}
func (r *MySQLUserRepo) CountUsersByRole(role string) (int, error) {
	var count int
	err := r.DB.QueryRow("SELECT COUNT(*) FROM users WHERE role = ?", role).Scan(&count)
	return count, err
}
func (r *MySQLUserRepo) GetOwnerByTowerAndFlat(tower string, flatNo string) (*domain.User, error) {
	row := r.DB.QueryRow("SELECT id, email FROM users WHERE tower = ? AND flat_no = ? AND role = 'owner'", tower, flatNo)
	var user domain.User
	err := row.Scan(&user.ID, &user.Email)
	if err != nil {
		return nil, err
	}
	return &user, nil
}
