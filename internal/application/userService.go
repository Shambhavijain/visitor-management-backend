package application

import (
	"errors"
	"fmt"
	"visitor-management/internal/domain"
	"visitor-management/internal/ports"

	"github.com/google/uuid"
)

type UserService struct {
	repo ports.UserRepository
}

func NewUserService(repo ports.UserRepository) *UserService {
	return &UserService{repo: repo}
}

func (s *UserService) GetallUsers() ([]domain.User, error) {
	fmt.Println("UserService: calling repo.GetallUsers")
	return s.repo.GetallUsers()
}

func (s *UserService) GetUserByUsername(email string) (*domain.User, error) {
	return s.repo.GetByEmail(email)
}

func (s *UserService) CreateUser(user domain.User) error {
	fmt.Println("Reached service to create user")

	user.ID = uuid.New().String()
	fmt.Println(user.ID)

	exists, err := s.repo.UsernameExists(user.Username)
	if err != nil {
		return err
	}
	if exists {
		return errors.New("username already exists")
	}

	return s.repo.Create(user)

}

func (s *UserService) GetUserById(userID string) (*domain.User, error) {
	fmt.Printf("Fetching user with ID: %s\n", userID)

	return s.repo.GetUserById(userID)
}
func (s *UserService) UpdateUser(user domain.User) error {
	return s.repo.UpdateUser(user)
}

func (s *UserService) DeleteUser(username string) error {
	return s.repo.Delete(username)
}
func (s *UserService) GetUserCountByRole(role string) (int, error) {
	return s.repo.CountUsersByRole(role)
}
