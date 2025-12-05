package utils

import (
	"fmt"
	"visitor-management/internal/config"

	"github.com/golang-jwt/jwt"
)

type JWTUserClaims struct {
	UserId string `json:"user_id"`
	Role   string `json:"role"`
	Email  string `json:"email"`
	jwt.StandardClaims
}

func ParseJWT(tokenString string) (*JWTUserClaims, error) {
	claims := &JWTUserClaims{}

	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		return config.JWTSecretKey, nil
	})
	if err != nil {
		return nil, err
	}

	if !token.Valid {
		return nil, fmt.Errorf("invalid token")
	}

	return claims, nil
}
