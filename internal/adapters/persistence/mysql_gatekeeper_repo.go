package persistence

import (
	"database/sql"
	"fmt"
	"visitor-management/internal/domain"
)

type GatekeeperRepo struct {
	DB *sql.DB
}

func NewGatekeeperRepo(db *sql.DB) *GatekeeperRepo {
	return &GatekeeperRepo{DB: db}
}

func (r *GatekeeperRepo) Create(g domain.Gatekeeper) error {

	query := `INSERT INTO users (id, username, email, password, address, role) VALUES (?, ?, ?, ?, ?, ?)`
	_, err := r.DB.Exec(query, g.ID, g.Username, g.Email, g.Password, g.Address, "gatekeeper")
	return err
}

func (r *GatekeeperRepo) Update(g domain.Gatekeeper) error {
	query := `UPDATE users SET email=?, password=?, address=? WHERE username=?`
	_, err := r.DB.Exec(query, g.Email, g.Password, g.Address, g.Username)
	return err
}

func (r *GatekeeperRepo) Delete(username string) error {
	query := `DELETE FROM users WHERE username=?`
	_, err := r.DB.Exec(query, username)
	return err
}

func (r *GatekeeperRepo) GetallGatekeepers() ([]domain.Gatekeeper, error) {
	fmt.Println("Reached  All Gatekeeper Repo")
	query := `SELECT username, email, password, address FROM users WHERE role='gatekeeper'`
	rows, err := r.DB.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var gatekeepers []domain.Gatekeeper
	for rows.Next() {
		var g domain.Gatekeeper
		if err := rows.Scan(&g.Username, &g.Email, &g.Password, &g.Address); err != nil {
			return nil, err
		}
		g.Role = "gatekeeper"
		gatekeepers = append(gatekeepers, g)
	}
	return gatekeepers, nil
}
func (r *GatekeeperRepo) CountGatekeeperByRole(role string) (int, error) {
	var count int
	err := r.DB.QueryRow("SELECT COUNT(*) FROM users WHERE role = ?", role).Scan(&count)
	return count, err
}
