package auth

import (
    "time"
    "github.com/golang-jwt/jwt/v5"
 "visitor-management/internal/config"
)

func GenerateJWT(userID string, role string) (string, error) {
    claims := jwt.MapClaims{
        "user_id": userID,
        "role": role,
        "exp": time.Now().Add(time.Hour * 1).Unix(),
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
     return token.SignedString(config.JWTSecretKey)
}
