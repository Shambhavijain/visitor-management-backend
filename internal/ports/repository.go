package ports

import "visitor-management/internal/domain"

type UserRepository interface {
	GetByEmail(email string) (*domain.User, error)
	Create(user domain.User) error
	UpdateUser(user domain.User) error
	Delete(username string) error
	GetallUsers() ([]domain.User, error)
	UsernameExists(username string) (bool, error)
	GetUserById(userid string) (*domain.User, error)
	CountUsersByRole(role string) (int, error)
	GetOwnerByTowerAndFlat(tower string, flatNo string) (*domain.User, error)
}

type GatekeeperRepository interface {
	Create(gatekeeper domain.Gatekeeper) error
	Update(gatekeeper domain.Gatekeeper) error
	Delete(username string) error
	GetallGatekeepers() ([]domain.Gatekeeper, error)
	CountGatekeeperByRole(role string) (int, error)
}

type VisitorRepository interface {
	Create(visitor *domain.Visitor) error
	Delete(id int) error
	GetVisitorsByOwner(ownerID string) ([]domain.Visitor, error)
	CountVisitors() (int, error)
	GetAllVisitors() ([]domain.Visitor, error)
	UpdateVisitorStatus(email, status string) error
}
