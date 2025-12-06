package application

import (
	"visitor-management/internal/domain"
	"visitor-management/internal/ports"

)


type GatekeeperService struct {
    Repo ports.UserRepository
}

func NewGatekeeperService(repo ports.UserRepository,) *GatekeeperService {
    return &GatekeeperService{Repo: repo}
}

// func (s *GatekeeperService) CreateGatekeeper(g domain.Gatekeeper) error {
//     g.ID=uuid.New().String();
//     return s.Repo.Create(g)
// }

// func (s *GatekeeperService) UpdateGatekeeper(g domain.Gatekeeper) error {
//     return s.Repo.Update(g)
// }

// func (s *GatekeeperService) DeleteGatekeeper(username string) error {
//     return s.Repo.Delete(username)
// }

func (s *GatekeeperService) GetAllGatekeepers() ([]domain.User, error) {
    users, err := s.Repo.GetallUsers()
    if err != nil {
        return nil, err
    }

    var gatekeepers []domain.User
    for _, u := range users {
        if u.Role == "gatekeeper" {
            gatekeepers = append(gatekeepers, u)
        }
    }

    return gatekeepers, nil
}
// func (s *GatekeeperService)CountGatekeeperByRole(role string)(int, error){
// return s.Repo.CountGatekeeperByRole(role)
// }