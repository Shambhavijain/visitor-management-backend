package domain

type Gatekeeper struct {
	ID       string `json:"-"`
	Role     string `json:"-"`
	Username string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
	Address  string `json:"address"`
}
