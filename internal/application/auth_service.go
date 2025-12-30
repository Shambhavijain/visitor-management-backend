package application

import (
	"fmt"
	userRepository "visitor-management/internal/adapters/repository"
	"visitor-management/internal/domain"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

type AuthService struct {
	userRepo *userRepository.UserRepo
}

func NewAuthService(repo *userRepository.UserRepo) *AuthService {
	return &AuthService{userRepo: repo}
}

func (s *AuthService) Login(email, password string) (*domain.User, error) {
	user, err := s.userRepo.GetByEmail(email)
	if err != nil {
		return nil, err
	}
	
	// fmt.Printf("Stored hashed password: %s\n", user.Password)
	// fmt.Printf("Provided password: %s\n", password)

	err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password))
	if err != nil {
		fmt.Println("Error comparing password:", err)
		return nil, fmt.Errorf("invalid credentials")
	}

	return user, nil
}

func (s *UserService) Signup(name, email, password, address, flat_no, tower string) error {

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
