package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"strings"
	userRepository "visitor-management/internal/adapters/repository"
	"visitor-management/internal/application"
	"visitor-management/internal/db"
	"visitor-management/internal/domain"
	"visitor-management/internal/middleware"
	"visitor-management/utils"

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

	authHeader := event.Headers["Authorization"]
	if authHeader == "" {
		return buildErrorResponse(401, "Authorization header missing"), nil
	}

	tokenString := strings.TrimPrefix(authHeader, "Bearer ")

	user, err := utils.ParseJWT(tokenString)
	if err != nil {
		return buildErrorResponse(401, "Invalid or expired token"), nil
	}

	if user.Role != "admin" {
		return buildErrorResponse(403, "You are not authorized to create gatekeepers"), nil
	}
	fmt.Println("  RAW REQUEST BODY:", event.Body)

	var gatekeeper domain.User
	err = json.Unmarshal([]byte(event.Body), &gatekeeper)
	if err != nil {
		return buildErrorResponse(400, "Invalid JSON body"), nil
	}
	fmt.Printf(" Parsed Gatekeeper Object: %+v\n", gatekeeper)

	gatekeeper.Role = "gatekeeper"

	err = userSvc.CreateGatekeeper(gatekeeper)
	if err != nil {
		log.Print(err)
		return buildErrorResponse(500, "Failed to create gatekeeper"), nil
	}

	resp, _ := json.Marshal(map[string]string{
		"message": "Gatekeeper created successfully",
	})

	return events.APIGatewayProxyResponse{
		StatusCode: 201,
		Body:       string(resp),
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
