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
	CreateGatekeeper(gatekeeper domain.User)error
}

// type GatekeeperRepository interface {
// 	// Create(gatekeeper domain.User) error
// 	// Update(gatekeeper domain.Gatekeeper) error
// 	// Delete(username string) error
// 	// GetallGatekeepers() ([]domain.Gatekeeper, error)
// }

type VisitorRepository interface {
	Create(visitor *domain.Visitor) error
	// Delete(id int) error
	GetVisitorsByOwner(ownerID string) ([]domain.Visitor, error)
	CountVisitors() (int, error)
	GetAllVisitors() ([]domain.Visitor, error)
	UpdateVisitorStatus(VisitorId string,OwnerId string, status string) error
}

