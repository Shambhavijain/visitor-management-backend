package domain

type Gatekeeper struct {
	ID   string `json:"user_id" dynamodbav:"UserId"`
	Role     string `json:"-" dynamodbav:"Role"`
	Username string `json:"username" dynamodbav:"Username"`
	Email    string `json:"email" dynamodbav:"Email"`
	Password string `json:"password,omitempty" dynamodbav:"Password"`
	Address  string `json:"address" dynamodbav:"Address"`
}

