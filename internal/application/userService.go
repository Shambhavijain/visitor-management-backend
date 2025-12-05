package application

import (
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
	users, err := s.repo.GetallUsers()
	if err != nil {
		return nil, err
	}

	var owners []domain.User
	for _, u := range users {
		if u.Role == "owner" {
			owners = append(owners, u)
		}
	}

	return owners, nil
}

func (s *UserService) GetUserByEmail(email string) (*domain.User, error) {
	return s.repo.GetByEmail(email)
}

func (s *UserService) CreateUser(user domain.User) error {
	fmt.Println("Reached service to create user")

	user.ID = uuid.New().String()
	fmt.Println(user.ID)

	return s.repo.Create(user)

}

func (s *UserService) GetUserById(userID string) (*domain.User, error) {
	fmt.Printf("Fetching user with ID: %s\n", userID)
	return s.repo.GetUserById(userID)
}
func (s *UserService) UpdateUser(user domain.User) error {
	return s.repo.UpdateUser(user)
}

func (s *UserService) DeleteUser(userId string) error {
	return s.repo.Delete(userId)
}

// func (s *UserService) GetUserCountByRole(role string) (int, error) {
// 	return s.repo.CountUsersByRole(role)
// }

func (s *UserService) GetUsersCount() (usercounts domain.UsersCount, err error) {
	return s.repo.GetUsersCount()
}
