package domain

type Visitor struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Email       string `json:"email"`
	Tower       string `json:"tower"`
	FlatNo      string `json:"flat_no"`
	AddedByRole string `json:"added_by_role"`
	Status      string `json:"status"`
	OwnerEmail  string `json:"owner_email"`
	OwnerID     string `json:"owner_id"`
	CreatedAt   int64  `json:"created_at"` 
}
