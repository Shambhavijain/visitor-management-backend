package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	userRepository "visitor-management/internal/adapters/repository"
	"visitor-management/internal/application"
	"visitor-management/internal/db"
	"visitor-management/internal/middleware"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

var userSvc *application.UserService

func init() {
	dynamoDB, err := db.InitDB()
	if err != nil {
		panic(fmt.Sprintf("Failed to initialize DB: %v", err))
	}

	tableName := "VMP_nosql"
	userRepo := userRepository.NewUserRepo(dynamoDB, tableName)

	userSvc = application.NewUserService(userRepo)
}

func main() {
	lambda.Start(middleware.WithCORS(Handler))
}

func Handler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	var req struct {
		Name     string `json:"name"`
		Email    string `json:"email"`
		Password string `json:"password"`
		Address  string `json:"address"`
		FlatNo   string `json:"flat_no"`
		Tower    string `json:"tower"`
	}

	if err := json.Unmarshal([]byte(event.Body), &req); err != nil {
		return buildErrorResponse(400, "Invalid request payload"), nil
	}

	err := userSvc.Signup(req.Name, req.Email, req.Password, req.Address, req.FlatNo, req.Tower)
	if err != nil {
		log.Print("Signup error:", err)
		return buildErrorResponse(500, err.Error()), nil
	}
	log.Printf("Signup DynamoDB error: %+v\n", err)

	return buildSuccessResponse(201, "Signup successful", nil), nil
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

func buildSuccessResponse(statusCode int, message string, data interface{}) events.APIGatewayProxyResponse {
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
