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
	lambda.Start(middleware.WithCORS(
		middleware.WithJWTContext(
			UpdateVisitorStatusHandler,
		),
	))
}

func UpdateVisitorStatusHandler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	userID := ctx.Value(middleware.UserIDKey).(string)
	role := ctx.Value(middleware.RoleKey).(string)

	if role != "owner" {
		return buildErrorResponse(403, "only owners can update visitor status"), nil
	}

	var req struct {
		VisitorID string `json:"visitor_id"`
		Status    string `json:"status"`
	}

	if err := json.Unmarshal([]byte(event.Body), &req); err != nil {
		return buildErrorResponse(400, "invalid request body"), nil
	}

	if req.VisitorID == "" {
		return buildErrorResponse(400, "visitor_id required"), nil
	}

	err := VisitorSvc.UpdateVisitorStatus(req.VisitorID, userID, req.Status)
	if err != nil {
		return buildErrorResponse(500, err.Error()), nil
	}

	return buildSuccessResponse(200, "status updated successfully"), nil
}
func buildErrorResponse(status int, msg string) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(map[string]string{"message": msg})
	return events.APIGatewayProxyResponse{StatusCode: status, Body: string(body)}
}

func buildSuccessResponse(status int, msg string) events.APIGatewayProxyResponse {
	body, _ := json.Marshal(map[string]interface{}{"message": msg})
	return events.APIGatewayProxyResponse{StatusCode: status, Body: string(body)}
}
