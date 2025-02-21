package main

import (
	"log"

	tea "github.com/charmbracelet/bubbletea"
)

func main() {
	config := LoadConfig()

	m := NewModel(config.APIURL)
	p := tea.NewProgram(m, tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		log.Fatal("Failed to start the TUI:", err)
	}
}
