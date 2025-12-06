package utils

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
)

func Migrate(db *sql.DB) error {

	schemaPath := filepath.Join("utils", "Schema.sql")
	schema, err := os.ReadFile(schemaPath)
	if err != nil {
		return fmt.Errorf("failed to read schema file: %v", err)
	}
	_, err = db.Exec(string(schema))
	if err != nil {
		return fmt.Errorf("failed to execute schema: %v", err)
	}

	fmt.Println("Migration completed successfully")
	return nil
}
