 package httpHandler

// import (
// 	"encoding/json"
// 	"fmt"
// 	"net/http"
// 	"visitor-management/internal/application"
// 	"visitor-management/internal/domain"
// )

// type GatekeeperHandler struct {
// 	Service *application.GatekeeperService
// }

// func NewGatekeeperHandler(s *application.GatekeeperService) *GatekeeperHandler {
// 	return &GatekeeperHandler{Service: s}
// }

// func (h *GatekeeperHandler) CreateGatekeeper(w http.ResponseWriter, r *http.Request) {
// 	var g domain.Gatekeeper
// 	if err := json.NewDecoder(r.Body).Decode(&g); err != nil {
// 		http.Error(w, err.Error(), http.StatusBadRequest)
// 		return
// 	}
// 	g.Role = "gatekeeper"
// 	if err := h.Service.CreateGatekeeper(g); err != nil {
// 		http.Error(w, err.Error(), http.StatusInternalServerError)
// 		return
// 	}
// 	w.WriteHeader(http.StatusCreated)
// }

// func (h *GatekeeperHandler) UpdateGatekeeper(w http.ResponseWriter, r *http.Request) {
// 	var g domain.Gatekeeper
// 	if err := json.NewDecoder(r.Body).Decode(&g); err != nil {
// 		http.Error(w, err.Error(), http.StatusBadRequest)
// 		return
// 	}
// 	if err := h.Service.UpdateGatekeeper(g); err != nil {
// 		http.Error(w, err.Error(), http.StatusInternalServerError)
// 		return
// 	}
// 	w.WriteHeader(http.StatusOK)
// }

// func (h *GatekeeperHandler) DeleteGatekeeper(w http.ResponseWriter, r *http.Request) {
	
// var req struct {
//         Username string `json:"username"`
//     }

// if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
//         http.Error(w, "Invalid request body", http.StatusBadRequest)
//         return
//     }

//  if req.Username == "" {
//         http.Error(w, "username is required", http.StatusBadRequest)
//         return
//     }

// 	if err := h.Service.DeleteGatekeeper(req.Username); err != nil {
// 		http.Error(w, err.Error(), http.StatusInternalServerError)
// 		return
// 	}
// 	w.Header().Set("Content-Type", "application/json")
// w.WriteHeader(http.StatusOK)
// w.Write([]byte(`{"message":"User deleted successfully"}`))

// }

// func (h *GatekeeperHandler) GetAllGatekeepers(w http.ResponseWriter, r *http.Request) {
// 	fmt.Println("HIT")
// 	gatekeepers, err := h.Service.GetAllGatekeepers()
// 	if err != nil {
// 		http.Error(w, err.Error(), http.StatusInternalServerError)
// 		return
// 	}
// 	json.NewEncoder(w).Encode(gatekeepers)
// }
// func (h *GatekeeperHandler) GetGatekeeperCount(w http.ResponseWriter, r *http.Request) {
//     count, err := h.Service.CountGatekeeperByRole("gatekeeper")
//     if err != nil {
//         http.Error(w, "Failed to get gatekeeper count", http.StatusInternalServerError)
//         return
//     }
//     json.NewEncoder(w).Encode(count)
// }



