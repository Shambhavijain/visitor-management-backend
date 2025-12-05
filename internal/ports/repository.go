package ports

import "visitor-management/internal/domain"

type UserRepository interface {
	GetByEmail(email string) (*domain.User, error)
	Create(user domain.User) error
	UpdateUser(user domain.User) error
	Delete(userId string) error
	GetallUsers() ([]domain.User, error)
	GetUserById(userid string) (*domain.User, error)
	GetOwnerByTowerAndFlat(tower string, flatNo string) (*domain.User, error)
	GetUsersCount() (UserCount domain.UsersCount, err error)
}

type GatekeeperRepository interface {
	Create(gatekeeper domain.Gatekeeper) error
	Update(gatekeeper domain.Gatekeeper) error
	Delete(username string) error
	GetallGatekeepers() ([]domain.Gatekeeper, error)
}

type VisitorRepository interface {
	Create(visitor *domain.Visitor) error
	// Delete(id int) error
	GetVisitorsByOwner(ownerID string) ([]domain.Visitor, error)
	CountVisitors() (int, error)
	GetAllVisitors() ([]domain.Visitor, error)
	UpdateVisitorStatus(VisitorId string,OwnerId string, status string) error // to do : send Visitor ID HERE UpdateVisitorStatus(VisitorID, OwnerID--from context, UpdatedSTatus)
}

/*
1.Domain Layer Consistent.
2.Services correspondingly refactor.
3. Swagger Docs: Check kro exact match (optional)
4. Json Format mein


{
	PK: "VISITORS"
	SK: "VISITOR#" + <Owner_Id>+ <Visitor_id>  
	ID: UUID (string) // Visitor ID
	Name        string    `json:"name"`
	Email       string    `json:"email"`
	Tower       string    `json:"tower"`
	FlatNo      string    `json:"flat_no"`
	AddedByRole string    `json:"added_by_role"`
	Status      string    `json:"status"`
	OwnerEmail  string    `json:"owner_email"`
	OwnerID     string
	OwnerId: UUID(string) 



	Create(visitor *domain.Visitor) error  (Make sure to store data in above shown schema)
	// Delete(id int) error
	GetVisitorsByOwner(ownerID string) ([]domain.Visitor, error)
	 ---->Query: PK= Visitors SK : Begins with "Visitor"#<OwnerId>

	GetAllVisitors() ([]domain.Visitor, error)
	--> Query PK= Visitors SK: Begins with

	CountVisitors() (int, error) (iske andr GetAllVisitors() ko reuse kr lena)
	--> query PK= Visitors SK: Begins with "Visitor"=> length calculate krke return krdo


	UpdateVisitorStatus(email, status string) error
	--> query (Update)
	Owner Id hogi kyuki Owner ka token h (context) -> Service will send
	Visitor ID-> Visitor Loaded hoga UI pe to wahaan se body mein bhejna

	QUery: PK: Visitors SK: "Visitor#"+ <OnwerId> + <VisitorId>


}
*/
