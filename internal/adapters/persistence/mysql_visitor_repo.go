 package persistence

// import (
// 	"database/sql"
// 	"fmt"
// 	"time"
// 	"visitor-management/internal/domain"
// )

// type MySQLVisitorRepository struct {
// 	DB *sql.DB
// }

// func NewMySQLVisitorRepo(db *sql.DB) *MySQLVisitorRepository {
// 	return &MySQLVisitorRepository{DB: db}
// }
// func (r *MySQLVisitorRepository) Create(visitor *domain.Visitor) error {
// 	query := `INSERT INTO visitors (id, name, email, tower, flat_no, added_by_role, status, owner_email, owner_id, created_at)
//               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
// 	_, err := r.DB.Exec(query, visitor.ID, visitor.Name, visitor.Email, visitor.Tower, visitor.FlatNo,
// 		visitor.AddedByRole, visitor.Status, visitor.OwnerEmail, visitor.OwnerID, visitor.CreatedAt)

// 	return err
// }

// func (r *MySQLVisitorRepository) Delete(id int) error {
// 	query := `DELETE FROM visitors WHERE id = ?`
// 	_, err := r.DB.Exec(query, id)
// 	return err
// }

// func (r *MySQLVisitorRepository) GetAllVisitors() ([]domain.Visitor, error) {
// 	rows, err := r.DB.Query("SELECT id, name, email, tower, flat_no, added_by_role, status, owner_email, owner_id, created_at FROM visitors")
// 	if err != nil {
// 		fmt.Printf("DB error in GetAll: %v\n", err)
// 		return nil, err
// 	}
// 	defer rows.Close()

// 	var visitors []domain.Visitor
// 	for rows.Next() {
// 		var v domain.Visitor
// 		var createdAtRaw []byte

// 		err := rows.Scan(&v.ID, &v.Name, &v.Email, &v.Tower, &v.FlatNo, &v.AddedByRole, &v.Status, &v.OwnerEmail, &v.OwnerID, &createdAtRaw)
// 		if err != nil {
// 			fmt.Printf("Scan error in GetAll: %v\n", err)
// 			return nil, err
// 		}

// 		v.CreatedAt, err = time.Parse("2006-01-02 15:04:05", string(createdAtRaw))
// 		if err != nil {
// 			fmt.Printf("Time parse error: %v\n", err)
// 			return nil, err
// 		}

// 		visitors = append(visitors, v)
// 	}

// 	return visitors, nil
// }

// func (r *MySQLVisitorRepository) GetVisitorsByOwner(ownerID string) ([]domain.Visitor, error) {
//     rows, err := r.DB.Query(`
//         SELECT id, name, email, tower, flat_no, added_by_role, status, owner_email, owner_id, created_at 
//         FROM visitors 
//         WHERE owner_id = ?`, ownerID)
//     if err != nil {
//         fmt.Printf("DB error in GetVisitorsByOwner: %v\n", err)
//         return nil, err
//     }
//     defer rows.Close()

//     var visitors []domain.Visitor
//     for rows.Next() {
//         var v domain.Visitor
//         var createdAtRaw []byte

//         err := rows.Scan(
//             &v.ID, &v.Name, &v.Email, &v.Tower, &v.FlatNo,
//             &v.AddedByRole, &v.Status, &v.OwnerEmail, &v.OwnerID, &createdAtRaw,
//         )
//         if err != nil {
//             fmt.Printf("Scan error in GetVisitorsByOwner: %v\n", err)
//             return nil, err
//         }

//         v.CreatedAt, err = time.Parse("2006-01-02 15:04:05", string(createdAtRaw))
//         if err != nil {
//             fmt.Printf("Time parse error in GetVisitorsByOwner: %v\n", err)
//             return nil, err
//         }

//         visitors = append(visitors, v)
//     }
//     return visitors, nil
// }
// func (r *MySQLVisitorRepository) CountVisitors() (int, error) {
// 	var count int
// 	err := r.DB.QueryRow("SELECT COUNT(*) FROM visitors WHERE status = 'approved'").Scan(&count)
// 	return count, err
// }
// func (r *MySQLVisitorRepository) UpdateVisitorStatus(email, status string) error {
// 	_, err := r.DB.Exec("UPDATE visitors SET status = ? WHERE email = ?", status, email)
// 	return err
// }
