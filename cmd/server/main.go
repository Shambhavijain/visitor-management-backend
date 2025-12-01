package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"

	"os"
	"visitor-management/internal/adapters/httpHandler"
	"visitor-management/internal/adapters/persistence"
	"visitor-management/internal/application"
	"visitor-management/internal/config"
	"visitor-management/internal/middleware"
	"visitor-management/utils"

	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
	"github.com/joho/godotenv"
)

func main() {

	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	// dbUser := os.Getenv("DB_USER")
	// dbPass := os.Getenv("DB_PASSWORD")
	// dbHost := os.Getenv("DB_HOST")
	// dbPort := os.Getenv("DB_PORT")
	// dbName := os.Getenv("DB_NAME")
	// dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", dbUser, dbPass, dbHost, dbPort, dbName)

	dsn := os.Getenv("DSN_STRING")
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal(err)
	}

	if err = db.Ping(); err != nil {
		log.Fatalf("DB ping error: %v", err)
	}

	fmt.Println("Connected to MySQL successfully!")

	if err := utils.Migrate(db); err != nil {
		log.Fatalf("Migration failed: %v", err)
	}
	owner := uuid.New().String()
	fmt.Println(owner)

	// Connect to MySQL
	// db, err := sql.Open("mysql", "root:Sh@mbhavi@03@tcp(127.0.0.1:3306)/visitor_mgmt")
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// if err = db.Ping(); err != nil {
	// 	log.Fatalf("DB ping error: %v", err)
	// }
	// fmt.Println(" Connection established with Database")

	userRepo := persistence.NewMySQLUserRepo(db)
	userService := application.NewUserService(userRepo)
	authService := application.NewAuthService(userRepo)
	userHandler := httpHandler.NewUserHandler(userService)
	authHandler := httpHandler.NewAuthHandler(authService)
	http.Handle("/signup", middleware.CORSMiddleware(http.HandlerFunc(userHandler.Signup)))
	http.Handle("/login", middleware.CORSMiddleware(http.HandlerFunc(authHandler.Login)))
	http.Handle("/users", middleware.CORSMiddleware(http.HandlerFunc(userHandler.ListUsers)))
	http.Handle("/delete-user", middleware.CORSMiddleware(http.HandlerFunc(userHandler.DeleteUser)))
	http.Handle("/users/", middleware.CORSMiddleware(http.HandlerFunc(userHandler.GetUserByID)))
	http.Handle("/update-user/", middleware.CORSMiddleware(http.HandlerFunc(userHandler.UpdateUser)))
	http.Handle("/getownercount", middleware.CORSMiddleware(http.HandlerFunc(userHandler.GetOwnerCount)))

	gatekeeperRepo := persistence.NewGatekeeperRepo(db)
	gatekeeperService := application.NewGatekeeperService(gatekeeperRepo)

	gatekeeperHandler := httpHandler.NewGatekeeperHandler(gatekeeperService)

	http.Handle("/create-gatekeeper", middleware.CORSMiddleware(http.HandlerFunc(gatekeeperHandler.CreateGatekeeper)))
	http.Handle("/update-gatekeeper", middleware.CORSMiddleware(http.HandlerFunc(gatekeeperHandler.UpdateGatekeeper)))
	http.Handle("/gatekeepers", middleware.CORSMiddleware(http.HandlerFunc(gatekeeperHandler.GetAllGatekeepers)))
	http.Handle("/delete-gatekeeper", middleware.CORSMiddleware(http.HandlerFunc(gatekeeperHandler.DeleteGatekeeper)))
	http.Handle("/getgatekeepercount", middleware.CORSMiddleware(http.HandlerFunc(gatekeeperHandler.GetGatekeeperCount)))

	visitorRepo := persistence.NewMySQLVisitorRepo(db)
	visitorService := application.NewVisitorService(visitorRepo, userRepo)
	visitorHandler := httpHandler.NewVisitorHandler(visitorService)

	http.Handle("/create-visitor", middleware.CORSMiddleware(middleware.AuthMiddleware(string(config.JWTSecretKey))(http.HandlerFunc(visitorHandler.CreateVisitor))))
	http.Handle("/update-visitor-status", middleware.CORSMiddleware(middleware.AuthMiddleware(string(config.JWTSecretKey))(http.HandlerFunc(visitorHandler.UpdateVisitorStatus))))
	http.Handle("/getvisitors", middleware.CORSMiddleware(middleware.AuthMiddleware(string(config.JWTSecretKey))(http.HandlerFunc(visitorHandler.GetVisitors))))
	http.Handle("/delete-visitor", middleware.CORSMiddleware(middleware.AuthMiddleware(string(config.JWTSecretKey))(http.HandlerFunc(visitorHandler.DeleteVisitor))))
	http.Handle("/visitors-by-owner", middleware.CORSMiddleware(middleware.AuthMiddleware(string(config.JWTSecretKey))(http.HandlerFunc(visitorHandler.GetVisitorsByOwner))))
	http.Handle("/getvisitorscount", middleware.CORSMiddleware(middleware.AuthMiddleware(string(config.JWTSecretKey))(http.HandlerFunc(visitorHandler.GetVisitorsCount))))

	log.Println("Server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
