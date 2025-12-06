package main

import (
	"context"
	"encoding/json"
	"fmt"
	userRepository "visitor-management/internal/adapters/repository"
	"visitor-management/internal/application"
	"visitor-management/internal/db"
	"visitor-management/internal/domain"
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
func main(){
	lambda.Start(middleware.WithCORS(
			middleware.WithJWTContext(
				CreateVisitorHandler,
			),
		),
	)
}
func CreateVisitorHandler(ctx context.Context, req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	var body domain.Visitor
	if err := json.Unmarshal([]byte(req.Body), &body); err != nil {
		return buildErrorResponse(400, "Invalid request body"), nil
	}

	userID, _ := middleware.GetUserIDFromContext(ctx)
	role, _ := middleware.GetRoleFromContext(ctx)

	createdVisitor, err := VisitorSvc.CreateVisitor(&body, userID, role)
	if err != nil {
		return buildErrorResponse(500, err.Error()), nil
	}

	
	return buildSuccessResponse(201, createdVisitor), nil
}



func buildErrorResponse(status int, msg string) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(map[string]string{"message": msg})
	return events.APIGatewayProxyResponse{StatusCode: status, Body: string(body)}
}

func buildSuccessResponse(status int, data interface{}) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(map[string]interface{}{"data": data})
	return events.APIGatewayProxyResponse{
		StatusCode: status,
		Body:       string(body),
	}
}

