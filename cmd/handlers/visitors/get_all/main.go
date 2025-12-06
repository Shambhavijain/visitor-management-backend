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

var VisitorSvc *application.VisitorService

func init() {
	dynamoDB, err := db.InitDB()
	if err != nil {
		panic(fmt.Sprintf("Failed to initialize DB: %v", err))
	}

	tableName := "VMP_nosql"

	VisitorRepo := userRepository.NewVisitorRepo(dynamoDB, tableName)
	UserRepo := userRepository.NewUserRepo(dynamoDB, tableName)

	VisitorSvc = application.NewVisitorService(VisitorRepo, UserRepo)
}
func main() {
	lambda.Start(
		middleware.WithCORS(
			middleware.WithJWTContext(
				GetAllVisitorsHandler,
			),
		),
	)
}

func GetAllVisitorsHandler(ctx context.Context, req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	visitors, err := VisitorSvc.GetAllVisitors()
	if err != nil {
		return buildErrorResponse(500, err.Error()), nil
	}

	return buildSuccessResponse(200, visitors), nil
}

func buildErrorResponse(status int, msg string) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(map[string]string{"message": msg})
	return events.APIGatewayProxyResponse{StatusCode: status, Body: string(body)}
}

func buildSuccessResponse(status int, data interface{}) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(data)
	return events.APIGatewayProxyResponse{
		StatusCode: status,
		Body:       string(body),
	}
}
