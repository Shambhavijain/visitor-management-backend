package middleware

import (
	"context"
	"fmt"
	"net/http"
	"strings"
	

	"github.com/golang-jwt/jwt"
)

type AuthenticatedUser struct {
	ID   string
	Role string
}

type contextKey string

const userContextKey = contextKey("user")

func AuthMiddleware(secretKey string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			fmt.Println("Auth Middleware called")
			tokenStr := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
fmt.Println(tokenStr)
			token, err := jwt.Parse(tokenStr, func(token *jwt.Token) (interface{}, error) {
    return []byte(secretKey), nil
})


			if err != nil || !token.Valid {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}

			claims, ok := token.Claims.(jwt.MapClaims)
			if !ok {
				http.Error(w, "Invalid token claims", http.StatusUnauthorized)
				return
			}

			user := &AuthenticatedUser{
				ID:   (claims["user_id"].(string)),
				Role: claims["role"].(string),
			}

			ctx := context.WithValue(r.Context(), userContextKey, user)
			fmt.Println("Auth Middleware passed, calling next handler")
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

func GetAuthenticatedUser(ctx context.Context) (*AuthenticatedUser, bool) {
	user, ok := ctx.Value(userContextKey).(*AuthenticatedUser)
	return user, ok
}
