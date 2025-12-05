package main

import (
	"context"
	"encoding/json"
	"fmt"

	userRepository "visitor-management/internal/adapters/repository"
	"visitor-management/internal/application"
	"visitor-management/internal/db"
	"visitor-management/internal/middleware"

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
	lambda.Start(middleware.WithCORS(GetUsersCountHandler))
}

func GetUsersCountHandler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	usersCount, err := userService.GetUsersCount()
	if err != nil {
		return buildErrorResponse(500, "Failed to get users count"), nil
	}

	payload := map[string]int{
		"owner":      usersCount.Owner,
		"gatekeeper": usersCount.Gatekeeper,
	}
	return buildResponse(200, payload), nil
}

func buildResponse(statusCode int, payload interface{}) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(payload)
	return events.APIGatewayProxyResponse{
		StatusCode: statusCode,
		Body:       string(body),
		Headers: map[string]string{
			"Content-Type":                 "application/json",
			"Access-Control-Allow-Origin":  "*",
			"Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
			"Access-Control-Allow-Methods": "OPTIONS,GET",
		},
	}
}

func buildErrorResponse(statusCode int, message string) events.APIGatewayProxyResponse {
	return buildResponse(statusCode, map[string]interface{}{
		"status_code": statusCode,
		"message":     message,
	})
}
