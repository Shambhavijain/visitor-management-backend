package main

import (
	"context"
	"encoding/json"
	"fmt"
	userRepository "visitor-management/internal/adapters/repository"
	"visitor-management/internal/application"
	"visitor-management/internal/db"
	"visitor-management/internal/domain"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

var userService *application.UserService

func init() {
	dynamoDB, err := db.InitDB()
	if err != nil {
		panic(fmt.Sprintf("Failed to initialize DB: %v", err))
	}
	userRepo := userRepository.NewUserRepo(dynamoDB, "VMP_nosql")
	userService = application.NewUserService(userRepo)
}

func main() {
	lambda.Start(CreateUserHandler)
}

func CreateUserHandler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	var user domain.User
	if err := json.Unmarshal([]byte(event.Body), &user); err != nil {
		return buildErrorResponse(400, "Invalid request payload"), nil
	}

	err := userService.CreateUser(user)
	if err != nil {
		return buildErrorResponse(500, err.Error()), nil
	}

	return events.APIGatewayProxyResponse{
		StatusCode: 201,
		Body:       `{"message":"User created successfully"}`,
	}, nil
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
