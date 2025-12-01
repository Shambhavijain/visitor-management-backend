package httpHandler

import (
	"encoding/json"
	"fmt"

	"net/http"
	"visitor-management/internal/adapters/auth"
	"visitor-management/internal/application"
)

type AuthHandler struct {
	authService *application.AuthService
}

func NewAuthHandler(service *application.AuthService) *AuthHandler {
	return &AuthHandler{authService: service}
}

func (h *AuthHandler) Login(w http.ResponseWriter, r *http.Request) {
	var req struct {
			Email string `json:"email"`
		Password string `json:"password"`
	}

	fmt.Println("Login attempt for user with email:", req.Email)
	_ = json.NewDecoder(r.Body).Decode(&req)
	user, err := h.authService.Login(req.Email, req.Password)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	token, _ := auth.GenerateJWT(user.ID, user.Role)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"token": token})
}
