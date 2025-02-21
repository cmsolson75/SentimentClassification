package main

import (
	"fmt"

	"github.com/charmbracelet/bubbles/textinput"
	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

type Styles struct {
	BorderColor lipgloss.Color
	InputField  lipgloss.Style
	OutputField lipgloss.Style
}

func DefaultStyles() *Styles {
	return &Styles{
		BorderColor: lipgloss.Color("38"),
		InputField: lipgloss.NewStyle().
			BorderForeground(lipgloss.Color("38")).
			BorderStyle(lipgloss.NormalBorder()).
			Padding(1).
			Width(80),
		OutputField: lipgloss.NewStyle().
			BorderForeground(lipgloss.Color("68")).
			BorderStyle(lipgloss.NormalBorder()).
			Padding(1).
			Width(80),
	}
}

type Model struct {
	styles    *Styles
	textField textinput.Model
	viewport  viewport.Model
	width     int
	height    int
	apiURL    string
}

func NewModel(apiURL string) *Model {
	styles := DefaultStyles()

	textField := textinput.New()
	textField.Placeholder = "Enter text for sentiment analysis"
	textField.Focus()

	vp := viewport.New(80, 3)

	return &Model{
		styles:    styles,
		textField: textField,
		viewport:  vp,
		apiURL:    apiURL,
	}
}

func (m Model) Init() tea.Cmd {
	return nil
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case tea.KeyMsg:
		switch msg.Type {
		case tea.KeyCtrlC, tea.KeyEsc:
			return m, tea.Quit
		case tea.KeyEnter:
			response, err := FetchSentimentAnalysis(m.apiURL, m.textField.Value())
			if err != nil {
				m.viewport.SetContent(fmt.Sprintf("Error: %v", err))
			} else {
				m.viewport.SetContent(
					fmt.Sprintf(
						"Prediction: %s %.1f%%",
						response.Label,
						response.Confidence*100,
					),
				)
			}
			m.textField.Reset()
		}
	}
	m.textField, cmd = m.textField.Update(msg)
	return m, cmd
}

func (m Model) renderTitle() string {
	return "📊 Sentiment Analysis Interface"
}

func (m Model) renderInput() string {
	return m.styles.InputField.Render(m.textField.View())
}

func (m Model) renderOutput() string {
	return m.styles.OutputField.Render(m.viewport.View())
}

func (m Model) View() string {
	content := lipgloss.JoinVertical(
		lipgloss.Center,
		m.renderTitle(),
		m.renderInput(),
		m.renderOutput(),
		"(Press ESC to quit)",
	)

	return lipgloss.Place(
		m.width,
		m.height,
		lipgloss.Center,
		lipgloss.Center,
		content,
	)
}
