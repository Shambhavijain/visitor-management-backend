package middleware

import (
	"context"
	"fmt"
	"log"
	"strings"
	"visitor-management/internal/config"

	"github.com/aws/aws-lambda-go/events"
	"github.com/golang-jwt/jwt/v5"
)


type ctxKey string

const (
	UserIDKey ctxKey = "userID"
	RoleKey   ctxKey = "role"
)

func WithJWTContext(next func(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error)) func(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	return func(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
		authHeader := event.Headers["Authorization"]
		if authHeader == "" {
			return buildErrorResponse(401, "Authorization header missing"), nil
		}
		log.Print(authHeader)
		tokenStr := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenStr == "" {
			return buildErrorResponse(401, "Bearer token missing"), nil
		}

		token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (interface{}, error) {
			if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
			}
			return []byte(config.JWTSecretKey), nil
		})
		log.Print(token)

		if err != nil || !token.Valid {
			return buildErrorResponse(401, "invalid token"), nil
		}

		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			return buildErrorResponse(401, "invalid token claims"), nil
		}

		if userID, ok := claims["user_id"].(string); ok && userID != "" {
			ctx = context.WithValue(ctx, UserIDKey, userID)
		} else {
			return buildErrorResponse(401, "user_id missing in token"), nil
		}

		if role, ok := claims["role"].(string); ok && role != "" {
			ctx = context.WithValue(ctx, RoleKey, role)
		}

		return next(ctx, event)
	}
}

func GetUserIDFromContext(ctx context.Context) (string, error) {
	userID, ok := ctx.Value(UserIDKey).(string)
	if !ok || userID == "" {
		return "", fmt.Errorf("userID not found in context")
	}
	return userID, nil
}

func GetRoleFromContext(ctx context.Context) (string, error) {
	role, ok := ctx.Value(RoleKey).(string)
	if !ok || role == "" {
		return "", fmt.Errorf("role not found in context")
	}
	return role, nil
}

func buildErrorResponse(status int, msg string) events.APIGatewayProxyResponse {
	return events.APIGatewayProxyResponse{
		StatusCode: status,
		Body:       fmt.Sprintf(`{"message":"%s"}`, msg),
	}
}
