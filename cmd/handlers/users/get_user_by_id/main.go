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

var userSvc *application.UserService

func init() {
	dynamoDB, err := db.InitDB()
	if err != nil {
		panic(fmt.Sprintf("Failed to intialize DB :%v", err))
	}
	tableName := "VMP_nosql"
	userRepo := userRepository.NewUserRepo(dynamoDB, tableName)
	userSvc = application.NewUserService(userRepo)
}

func main() {
	fmt.Println("Lambda starting…")
	lambda.Start(middleware.WithCORS(middleware.WithJWTContext(Handler)))
}
func Handler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	userID := event.PathParameters["user_id"]
	if userID == "" {
		return buildErrorResponse(400, "User ID not provided"), nil
	}

	// authHeader := event.Headers["Authorization"]
	// if authHeader == "" {
	// 	return buildErrorResponse(401, "Authorization header missing"), nil
	// }
	// tokenString := strings.TrimPrefix(authHeader, "Bearer ")

	// _, err := utils.ParseJWT(tokenString)
	// if err != nil {
	// 	return buildErrorResponse(401, "Invalid token"), nil
	// }
	user, err := userSvc.GetUserById(userID)
	if err != nil {
		return buildErrorResponse(500, "Error fetching user"), nil
	}
	if user == nil {
		return buildErrorResponse(404, "User not found"), nil
	}
	return buildSuccessResponse(200, "User fteched successfully", user), nil
}

func buildErrorResponse(status int, msg string) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(map[string]string{"message": msg})
	return events.APIGatewayProxyResponse{StatusCode: status, Body: string(body)}
}

func buildSuccessResponse(status int, msg string, data interface{}) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(map[string]interface{}{"message": msg, "data": data})
	return events.APIGatewayProxyResponse{StatusCode: status, Body: string(body)}
}
