 package httpHandler

// import (
// 	"encoding/json"
// 	"fmt"
// 	"log"
// 	"net/http"
// 	"strings"

// 	"visitor-management/internal/application"
// 	"visitor-management/internal/domain"

// 	"github.com/gorilla/mux"
// )

// type UserHandler struct {
// 	service *application.UserService
// }

// func NewUserHandler(service *application.UserService) *UserHandler {
// 	return &UserHandler{service: service}
// }
// func (h *UserHandler) Signup(w http.ResponseWriter, r *http.Request) {
// 	fmt.Println("HIT")
// 	fmt.Println("Reached handler to create user")
// 	var input struct {
// 		Name     string `json:"name"`
// 		Email    string `json:"email"`
// 		Password string `json:"password"`
// 		Address  string `json:"address"`
// 		FlatNo   string `json:"flat_no"`
// 		Tower    string `json:"tower"`
// 	}

// 	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
// 		http.Error(w, "Invalid input", http.StatusBadRequest)
// 		return
// 	}

// 	err := h.service.Signup(input.Name, input.Email, input.Password, input.Address, input.FlatNo, input.Tower)

// 	if err != nil {
// 		fmt.Println("Signup error:", err)
// 		if err.Error() == "username already exists" {
// 			http.Error(w, err.Error(), http.StatusConflict)
// 		} else {
// 			http.Error(w, "Signup failed", http.StatusInternalServerError)
// 		}
// 		return
// 	}

// 	w.Header().Set("Content-Type", "application/json")
// 	w.WriteHeader(http.StatusCreated)
// 	json.NewEncoder(w).Encode(map[string]string{
// 		"message": "Signup successful",
// 	})

// }
// func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
// 	fmt.Println("Hit get user")
// 	username := mux.Vars(r)["username"]
// 	user, err := h.service.GetUserByUsername(username)
// 	if err != nil {

// 		http.Error(w, "User not found", http.StatusNotFound)
// 		log.Println("Error in GetallUsers:", err)
// 		return
// 	}
// 	json.NewEncoder(w).Encode(user)
// }

// func (h *UserHandler) GetUserByID(w http.ResponseWriter, r *http.Request) {

// 	fmt.Println("Hit get user by id")
// 	path := r.URL.Path
// 	parts := strings.Split(path, "/")
// 	if len(parts) < 3 {
// 		http.Error(w, "User ID not provided", http.StatusBadRequest)
// 		return
// 	}

// 	idStr := parts[2]
// 	userID := idStr

// 	fmt.Println("Hit get user by id", userID)

// 	user, err := h.service.GetUserById(userID)
// 	if err != nil {
// 		http.Error(w, "Error fetching user", http.StatusInternalServerError)
// 		return
// 	}
// 	if user == nil {
// 		http.Error(w, "User not found", http.StatusNotFound)
// 		return
// 	}

// 	w.Header().Set("Content-Type", "application/json")
// 	json.NewEncoder(w).Encode(user)
// }
// func (h *UserHandler) ListUsers(w http.ResponseWriter, r *http.Request) {

// 	users, err := h.service.GetallUsers()
// 	if err != nil {
// 		http.Error(w, "Failed to fetch users", http.StatusInternalServerError)
// 		return
// 	}

// 	w.Header().Set("Content-Type", "application/json")
// 	json.NewEncoder(w).Encode(users)
// }
// func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
// 	var user domain.User
// 	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
// 		http.Error(w, "Invalid input", http.StatusBadRequest)
// 		return
// 	}
// 	err := h.service.CreateUser(user)

// 	if err != nil {
// 		if err.Error() == "username already exists" {
// 			http.Error(w, err.Error(), http.StatusConflict)
// 		} else {
// 			http.Error(w, "Failed to create user", http.StatusInternalServerError)
// 		}
// 		return
// 	}

// 	w.WriteHeader(http.StatusCreated)
// }

// func (h *UserHandler) UpdateUser(w http.ResponseWriter, r *http.Request) {
// 	fmt.Println("Hit update user")
// 	path := r.URL.Path
// 	parts := strings.Split(path, "/")
// 	if len(parts) < 3 {
// 		http.Error(w, "User ID not provided", http.StatusBadRequest)
// 		return
// 	}

// 	idStr := parts[2]
// 	userID := idStr

// 	var user domain.User
// 	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
// 		http.Error(w, "Invalid input", http.StatusBadRequest)
// 		return
// 	}

// 	user.ID = userID

// 	if err := h.service.UpdateUser(user); err != nil {
// 		http.Error(w, "Failed to update user", http.StatusInternalServerError)
// 		return
// 	}

// 	w.WriteHeader(http.StatusOK)
// }
// func (h *UserHandler) DeleteUser(w http.ResponseWriter, r *http.Request) {
// 	log.Println("Delete user hit")
// 	var input struct {
// 		Username string `json:"username"`
// 	}

// 	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
// 		http.Error(w, "Invalid input", http.StatusBadRequest)
// 		return
// 	}

// 	err := h.service.DeleteUser(input.Username)
// 	if err != nil {
// 		http.Error(w, "Failed to delete user", http.StatusInternalServerError)
// 		return
// 	}

// 	w.Header().Set("Content-Type", "application/json")
// 	w.WriteHeader(http.StatusOK)
// 	w.Write([]byte(`{"message":"User deleted successfully"}`))
// }
// func (h *UserHandler) GetOwnerCount(w http.ResponseWriter, r *http.Request) {
// 	count, err := h.service.GetUserCountByRole("owner")
// 	if err != nil {
// 		http.Error(w, "Failed to get owner count", http.StatusInternalServerError)
// 		return
// 	}
// 	json.NewEncoder(w).Encode(count)
// }
