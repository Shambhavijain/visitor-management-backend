package application

import (
	"visitor-management/internal/domain"
	"visitor-management/internal/ports"

	"github.com/google/uuid"
)


type GatekeeperService struct {
    Repo ports.GatekeeperRepository
}

func NewGatekeeperService(repo ports.GatekeeperRepository) *GatekeeperService {
    return &GatekeeperService{Repo: repo}
}

func (s *GatekeeperService) CreateGatekeeper(g domain.Gatekeeper) error {
    g.ID=uuid.New().String();
    return s.Repo.Create(g)
}

func (s *GatekeeperService) UpdateGatekeeper(g domain.Gatekeeper) error {
    return s.Repo.Update(g)
}

func (s *GatekeeperService) DeleteGatekeeper(username string) error {
    return s.Repo.Delete(username)
}

func (s *GatekeeperService) GetAllGatekeepers() ([]domain.Gatekeeper, error) {
    return s.Repo.GetallGatekeepers()
}
func (s *GatekeeperService)CountGatekeeperByRole(role string)(int, error){
return s.Repo.CountGatekeeperByRole(role)
}