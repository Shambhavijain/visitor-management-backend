package application

import (
	"errors"
	"fmt"
	"visitor-management/internal/domain"
	"visitor-management/internal/ports"

	"github.com/google/uuid"
)

type AuthService struct {
	userRepo ports.UserRepository
}

func NewAuthService(repo ports.UserRepository) *AuthService {
	return &AuthService{userRepo: repo}
}

func (a *AuthService) Login(email, password string) (*domain.User, error) {
	user, err := a.userRepo.GetByEmail(email)
	if err != nil {
		return nil, errors.New("user not found")
	}

	if user.Password != password {
		return nil, fmt.Errorf("invalid password")
	}

	return user, nil
}

func (s *UserService) Signup(name, email, password, address, flat_no, tower string) error {

	exists, err := s.repo.UsernameExists(name)
	if err != nil {
		return err
	}
	if exists {
		return errors.New("username already exists")
	}

	user := domain.User{
		ID:       uuid.New().String(),
		Username: name,
		Email:    email,
		Password: password,
		Address:  address,
		Role:     "owner",
		FlatNo:   flat_no,
		Tower:    tower,
	}
	return s.repo.Create(user)
}
