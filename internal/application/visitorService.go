package application

import (
	"fmt"
	"time"
	"visitor-management/internal/domain"
	"visitor-management/internal/ports"

	"github.com/google/uuid"
)

type VisitorService struct {
	Repo     ports.VisitorRepository
	UserRepo ports.UserRepository
}

func NewVisitorService(repo ports.VisitorRepository, UserRepo ports.UserRepository) *VisitorService {
	return &VisitorService{Repo: repo, UserRepo: UserRepo}
}

func (s *VisitorService) CreateVisitor(v *domain.Visitor, userID string, role string) (*domain.Visitor, error) {

	v.ID = uuid.New().String() // visitor_id
	v.CreatedAt = time.Now().Unix()
	v.AddedByRole = role

	if role == "owner" {
		v.OwnerID = userID

		user, err := s.UserRepo.GetUserById(userID)
		if err != nil {
			return nil, fmt.Errorf("failed to fetch user: %w", err)
		}

		v.OwnerEmail = user.Email

	} else {

		owner, err := s.UserRepo.GetOwnerByTowerAndFlat(v.Tower, v.FlatNo)
		if err != nil {
			return nil, fmt.Errorf("failed to find owner: %w", err)
		}

		v.OwnerID = owner.ID
		v.OwnerEmail = owner.Email
	}

	if role == "admin" || role == "owner" {
		v.Status = "approved"
	} else {
		v.Status = "pending"
	}

	// Save to DynamoDB
	err := s.Repo.Create(v)
	if err != nil {
		return nil, err
	}

	// Return the full visitor object including ID
	return v, nil
}

// func (s *VisitorService) DeleteVisitor(id int) error {
// 	return s.Repo.Delete(id)
// }

func (s *VisitorService) GetAllVisitors() ([]domain.Visitor, error) {
	visitors, err := s.Repo.GetAllVisitors()
	if err != nil {
		fmt.Printf("Service error in GetAllVisitors: %v\n", err)
	}
	return visitors, err
}

func (s *VisitorService) GetVisitorsByOwner(ownerID string) ([]domain.Visitor, error) {
	visitors, err := s.Repo.GetVisitorsByOwner(ownerID)
	if err != nil {
		fmt.Printf("Service error in GetVisitorsByOwner (ownerID=%s): %v\n", ownerID, err)
	}
	return visitors, err
}
func (s *VisitorService) GetVisitorCount() (int, error) {
	return s.Repo.CountVisitors()
}
func (s *VisitorService) UpdateVisitorStatus(visitorID, ownerID, status string) error {

	return s.Repo.UpdateVisitorStatus(visitorID, ownerID, status)
}
