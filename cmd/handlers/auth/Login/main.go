package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"visitor-management/internal/adapters/auth"
	userRepository "visitor-management/internal/adapters/repository"
	"visitor-management/internal/application"
	"visitor-management/internal/db"
	"visitor-management/internal/middleware"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

var authSvc *application.AuthService

func init() {
	dynamoDB, err := db.InitDB()
	if err != nil {
		panic(fmt.Sprintf("Failed to initialize DB: %v", err))
	}
	tableName := "VMP_nosql"
	userRepo := userRepository.NewUserRepo(dynamoDB, tableName)
	authSvc = application.NewAuthService(userRepo)
}

func main() {
	lambda.Start(middleware.WithCORS(Handler))
}

func Handler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	var req struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	log.Print(event)

	if err := json.Unmarshal([]byte(event.Body), &req); err != nil {
		return buildErrorResponse(400, "Invalid request payload"), nil
	}

	user, err := authSvc.Login(req.Email, req.Password)
	log.Print(user)
	if err != nil {
		log.Print(err)
		return buildErrorResponse(401, "Invalid email or password"), nil
	}

	token, err := auth.GenerateJWT(user.ID, user.Role)
	if err != nil {
		return buildErrorResponse(500, "Failed to generate token"), nil
	}

	data := map[string]interface{}{
		"token": token,
		"role":  user.Role,
	}

	if user.Role == "owner" {
		data["tower"] = user.Tower
		data["flat_no"] = user.FlatNo
	}

	return buildSuccessResponse(200, "Login successful", data), nil

}

func buildErrorResponse(statusCode int, message string) events.APIGatewayProxyResponse {
	resp := map[string]interface{}{
		"status_code": statusCode,
		"message":     message,
	}
	body, _ := json.Marshal(resp)

	return events.APIGatewayProxyResponse{
		StatusCode: statusCode,
		Body:       string(body),
	}
}

func buildSuccessResponse(statusCode int, message string, data map[string]any) events.APIGatewayProxyResponse {
	resp := map[string]interface{}{
		"status_code": statusCode,
		"message":     message,
		"data":        data,
	}
	body, _ := json.Marshal(resp)

	return events.APIGatewayProxyResponse{
		StatusCode: statusCode,
		Body:       string(body),
	}
}
