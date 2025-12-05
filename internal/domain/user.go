package domain

type User struct {
	ID       string `json:"userid"   dynamodbav:"UserId"`
	Username string `json:"username" dynamodbav:"Username"`
	Role     string `json:"role"     dynamodbav:"Role"`
	Email    string `json:"email"    dynamodbav:"Email"`
	Password string `json:"-"        dynamodbav:"Password"`
	Address  string `json:"address"  dynamodbav:"Address"`
	FlatNo   string `json:"flat_no"  dynamodbav:"Flat_no"`
	Tower    string `json:"tower"    dynamodbav:"Tower"`
}

type UsersCount struct {
    Owner      int `json:"owner"`
    Gatekeeper int `json:"gatekeeper"`
}
