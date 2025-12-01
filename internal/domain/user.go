package domain

type User struct {
	ID       string    `json:"-"`
	Username string `json:"username"`
	Role     string `json:"role"`
	Email    string `json:"email"`
	Password string `json:"-"` 
	Address  string `json:"address"`
	FlatNo string `json:"flat_no"`
	Tower string `json:"tower"`
}
