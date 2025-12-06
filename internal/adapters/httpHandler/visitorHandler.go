 package httpHandler

// import (
// 	"encoding/json"
// 	"fmt"
// 	"net/http"
// 	"strconv"
// 	"visitor-management/internal/application"
// 	"visitor-management/internal/domain"
// 	"visitor-management/internal/middleware"
// )

// type VisitorHandler struct {
// 	service *application.VisitorService
// }

// func NewVisitorHandler(service *application.VisitorService) *VisitorHandler {
// 	return &VisitorHandler{service: service}
// }

// func (h *VisitorHandler) CreateVisitor(w http.ResponseWriter, r *http.Request) {
// 	var v domain.Visitor
// 	if err := json.NewDecoder(r.Body).Decode(&v); err != nil {
// 		http.Error(w, "Invalid input", http.StatusBadRequest)
// 		return
// 	}

// 	user, ok := middleware.GetAuthenticatedUser(r.Context())
// 	if !ok {
// 		http.Error(w, "Unauthorized", http.StatusUnauthorized)
// 		return
// 	}

// 	err := h.service.CreateVisitor(&v, user.ID, user.Role)
// 	if err != nil {
// 		fmt.Printf("Error creating visitor: %v\n", err)
// 		http.Error(w, "Failed to create visitor", http.StatusInternalServerError)
// 		return
// 	}

// 	w.Header().Set("Content-Type", "application/json")
// 	json.NewEncoder(w).Encode(v)
// }
// func (h *VisitorHandler) DeleteVisitor(w http.ResponseWriter, r *http.Request) {
// 	idStr := r.URL.Query().Get("id")
// 	id, err := strconv.Atoi(idStr)
// 	if err != nil {
// 		http.Error(w, "Invalid visitor ID", http.StatusBadRequest)
// 		return
// 	}

// 	err = h.service.DeleteVisitor(id)
// 	if err != nil {
// 		http.Error(w, "Failed to delete visitor", http.StatusInternalServerError)
// 		return
// 	}

// 	w.WriteHeader(http.StatusNoContent)
// }
// func (h *VisitorHandler) GetVisitorsByOwner(w http.ResponseWriter, r *http.Request) {
// 	user, ok := middleware.GetAuthenticatedUser(r.Context())
// 	if !ok || user.Role != "owner" {
// 		http.Error(w, "Unauthorized", http.StatusUnauthorized)
// 		return
// 	}

// 	visitors, err := h.service.GetVisitorsByOwner(user.ID)
// 	if err != nil {
// 		http.Error(w, "Failed to fetch visitors", http.StatusInternalServerError)
// 		return
// 	}

// 	w.Header().Set("Content-Type", "application/json")
// 	json.NewEncoder(w).Encode(visitors)
// }
// func (h *VisitorHandler) GetVisitorsCount(w http.ResponseWriter, r *http.Request) {
// 	count, err := h.service.GetVisitorCount()
// 	if err != nil {
// 		http.Error(w, "Failed to get visitor count", http.StatusInternalServerError)
// 		return
// 	}
// 	json.NewEncoder(w).Encode(count)
// }
// func (h *VisitorHandler) GetVisitors(w http.ResponseWriter, r *http.Request) {
// 	fmt.Println("Reached here to fetch visitors")
// 	user, ok := middleware.GetAuthenticatedUser(r.Context())
// 	if !ok {
// 		http.Error(w, "Unauthorized", http.StatusUnauthorized)
// 		return
// 	}

// 	var visitors []domain.Visitor
// 	var err error

// 	if user.Role == "admin" || user.Role == "gatekeeper" {
// 		visitors, err = h.service.GetAllVisitors()
// 	} else {
// 		visitors, err = h.service.GetVisitorsByOwner(user.ID)
// 	} 

// 	if err != nil {
// 		fmt.Printf("Error fetching visitors for role %s and user ID %s: %v\n", user.Role, user.ID, err)
// 		http.Error(w, "Failed to fetch visitors", http.StatusInternalServerError)
// 		return
// 	}

// 	w.Header().Set("Content-Type", "application/json")
// 	json.NewEncoder(w).Encode(visitors)
// }
// func (h *VisitorHandler) UpdateVisitorStatus(w http.ResponseWriter, r *http.Request) {
// 	user, ok := middleware.GetAuthenticatedUser(r.Context())
// 	if !ok {
// 		http.Error(w, "Unauthorized", http.StatusUnauthorized)
// 		return
// 	}

// 	var req struct {
// 		Email  string `json:"email"`
// 		Status string `json:"status"`
// 	}

// 	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
// 		http.Error(w, "Invalid input", http.StatusBadRequest)
// 		return
// 	}

// 	err := h.service.UpdateVisitorStatus(req.Email, req.Status, user.ID, user.Role)
// 	if err != nil {
// 		http.Error(w, "Failed to update status", http.StatusInternalServerError)
// 		return
// 	}

// 	w.WriteHeader(http.StatusOK)
// }
