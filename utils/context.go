package utils

import (
	"context"
	"fmt"
)

func GetUserIDFromContext(ctx context.Context) (string, error) {
	userID, ok := ctx.Value("userID").(string)
	if !ok || userID == "" {
		return "", fmt.Errorf("userID not found in context")
	}
	return userID, nil
}
