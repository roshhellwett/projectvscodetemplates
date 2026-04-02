"""Interactive quiz for preset recommendations."""

from dataclasses import dataclass, field
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from projectvscodetemplates.presets import PresetManager, Preset, get_preset_manager
from projectvscodetemplates.utils import (
    print_info,
    print_success,
    print_warning,
    truncate_string,
    get_terminal_width,
)
from projectvscodetemplates.constants import (
    DIFFICULTY_COLORS,
    QUIZ_SCORE_TAG_EXACT,
    QUIZ_SCORE_TAG_PARTIAL,
    QUIZ_SCORE_CATEGORY,
    QUIZ_SCORE_DIFFICULTY,
    QUIZ_SCORE_LANGUAGE,
    QUIZ_SCORE_BASE,
    QUIZ_MIN_CONFIDENCE,
)

console = Console()


@dataclass
class QuizQuestion:
    """Represents a quiz question."""

    id: str
    question: str
    options: list[str]
    tags: list[list[str]]
    multi_select: bool = False
    required: bool = True
    weight: float = 1.0


@dataclass
class RecommendationResult:
    """A preset recommendation with confidence score."""

    preset: Preset
    score: float
    confidence: float
    match_reasons: list[str]
    tag_matches: dict[str, int]

    def __str__(self) -> str:
        return f"{self.preset.name} ({self.confidence:.0%} match)"


@dataclass
class QuizSession:
    """Tracks a quiz session."""

    questions_answered: int = 0
    total_questions: int = 0
    selected_options: dict[str, list[int]] = field(default_factory=dict)
    start_time: float = 0
    end_time: float = 0

    @property
    def duration_seconds(self) -> float:
        """Get quiz duration in seconds."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return 0

    @property
    def completion_rate(self) -> float:
        """Get completion rate."""
        if self.total_questions == 0:
            return 0
        return self.questions_answered / self.total_questions


class QuizEngine:
    """Manages the interactive preset recommendation quiz."""

    QUESTIONS: list[QuizQuestion] = [
        QuizQuestion(
            id="role",
            question="What best describes your role?",
            options=[
                "Student learning to code",
                "Professional developer",
                "Hobbyist / Enthusiast",
                "Content creator / Streamer",
            ],
            tags=[
                ["student", "beginner", "learning"],
                ["professional", "career"],
                ["hobby", "personal"],
                ["streaming", "youtube", "content"],
            ],
            weight=2.0,
        ),
        QuizQuestion(
            id="primary_language",
            question="Which programming language do you use most?",
            options=[
                "Python",
                "JavaScript / TypeScript",
                "Java",
                "C / C++",
                "Go",
                "Rust",
                "Other / Multiple",
            ],
            tags=[
                ["python"],
                ["javascript", "typescript", "react", "vue", "frontend"],
                ["java"],
                ["cpp", "c", "systems"],
                ["go", "golang"],
                ["rust"],
                ["general"],
            ],
            weight=3.0,
        ),
        QuizQuestion(
            id="focus_area",
            question="What's your primary focus area?",
            options=[
                "Web Development",
                "Data Science / ML",
                "Systems Programming",
                "Mobile Development",
                "Competitive Programming",
                "DevOps / Cloud",
                "Writing / Documentation",
            ],
            tags=[
                ["web", "frontend", "fullstack"],
                ["data", "ml", "jupyter", "pandas"],
                ["systems", "embedded", "cmake"],
                ["mobile", "flutter"],
                ["competitive", "dsa", "algorithms"],
                ["devops", "docker", "kubernetes", "cloud"],
                ["writing", "minimal", "zen"],
            ],
            weight=3.0,
        ),
        QuizQuestion(
            id="workstyle",
            question="How do you primarily work?",
            options=[
                "Local development",
                "Remote servers via SSH",
                "Mix of both",
            ],
            tags=[
                ["local"],
                ["remote", "ssh", "server"],
                ["mixed"],
            ],
            weight=1.5,
        ),
        QuizQuestion(
            id="experience",
            question="What's your experience level?",
            options=[
                "Beginner (less than 1 year)",
                "Intermediate (1-3 years)",
                "Advanced (3+ years)",
                "Expert / Professional",
            ],
            tags=[
                ["beginner"],
                ["intermediate"],
                ["advanced"],
                ["professional"],
            ],
            weight=2.0,
        ),
        QuizQuestion(
            id="preferences",
            question="What features matter most to you?",
            options=[
                "Auto-formatting & code quality",
                "Fast execution & debugging",
                "Rich code snippets & templates",
                "Beautiful themes & UI",
            ],
            tags=[
                ["formatting", "linting", "quality"],
                ["debugging", "performance", "testing"],
                ["snippets", "templates", "productivity"],
                ["theme", "icons", "appearance"],
            ],
            multi_select=True,
            weight=1.5,
        ),
    ]

    def __init__(self, preset_manager: PresetManager | None = None):
        """Initialize the quiz engine."""
        self._preset_manager = preset_manager
        self.answers: dict[str, list[str]] = {}
        self.collected_tags: list[str] = []
        self.tag_weights: dict[str, float] = {}
        self.session = QuizSession(total_questions=len(self.QUESTIONS))

    @property
    def preset_manager(self) -> PresetManager:
        """Get preset manager with lazy loading."""
        if self._preset_manager is None:
            self._preset_manager = get_preset_manager()
        return self._preset_manager

    def reset(self) -> None:
        """Reset quiz state."""
        self.answers = {}
        self.collected_tags = []
        self.tag_weights = {}
        self.session = QuizSession(total_questions=len(self.QUESTIONS))

    def run_question(self, question: QuizQuestion) -> None:
        """Run a single quiz question."""
        console.print()
        console.print(
            f"[bold cyan]Question {self.session.questions_answered + 1}/{self.session.total_questions}:[/] {question.question}"
        )
        console.print()

        for i, option in enumerate(question.options, 1):
            console.print(f"  [yellow]{i}.[/] {option}")

        console.print()

        while True:
            try:
                multi_hint = "(comma-separated for multiple) " if question.multi_select else ""
                response = input(f"  Your choice(s) {multi_hint}: ").strip()

                if not response:
                    if question.required:
                        print_warning("This question requires a response.")
                        continue
                    else:
                        break

                if question.multi_select:
                    indices = self._parse_multi_select(response, len(question.options))
                    if indices is None:
                        continue

                    self.answers[question.id] = [question.options[i - 1] for i in indices]
                    self.session.selected_options[question.id] = indices

                    for idx in indices:
                        for tag in question.tags[idx - 1]:
                            self.collected_tags.append(tag)
                            self.tag_weights[tag] = self.tag_weights.get(tag, 0) + question.weight
                else:
                    if not response.isdigit():
                        print_warning("Please enter a number")
                        continue

                    choice = int(response)
                    if not 1 <= choice <= len(question.options):
                        print_warning(
                            f"Please enter a number between 1 and {len(question.options)}"
                        )
                        continue

                    self.answers[question.id] = [question.options[choice - 1]]
                    self.session.selected_options[question.id] = [choice]

                    for tag in question.tags[choice - 1]:
                        self.collected_tags.append(tag)
                        self.tag_weights[tag] = self.tag_weights.get(tag, 0) + question.weight

                self.session.questions_answered += 1
                break
            except ValueError:
                print_warning("Invalid input. Please try again.")
            except (KeyboardInterrupt, EOFError):
                console.print()
                print_warning("Quiz interrupted.")
                raise

    def _parse_multi_select(self, response: str, max_options: int) -> list[int] | None:
        """Parse multi-select input into list of indices."""
        indices = []
        for char in response.replace(",", " ").replace(";", " ").split():
            if char.isdigit():
                idx = int(char)
                if 1 <= idx <= max_options:
                    indices.append(idx)

        if not indices:
            print_warning("Please enter valid number(s)")
            return None

        return sorted(set(indices))

    def run_quiz(self) -> list[RecommendationResult]:
        """Run the full quiz and return recommended presets."""
        import time

        self.reset()
        self.session.start_time = time.time()

        console.print()
        console.print("[bold magenta]" + "═" * 50 + "[/]")
        console.print("[bold magenta]    Find Your Perfect VS Code Preset[/]")
        console.print("[bold magenta]" + "═" * 50 + "[/]")
        console.print()
        console.print("[dim]Answer a few questions to get personalized recommendations[/dim]")
        console.print()

        try:
            for question in self.QUESTIONS:
                self.run_question(question)
        except KeyboardInterrupt:
            console.print()
            print_warning("Quiz cancelled by user.")
            return []

        self.session.end_time = time.time()
        console.print()
        console.print("[bold green]Analyzing your answers...[/]")
        console.print()

        recommendations = self._calculate_recommendations()

        return recommendations

    def _calculate_recommendations(self) -> list[RecommendationResult]:
        """Calculate preset recommendations with confidence scoring."""
        if not self.collected_tags:
            presets = self.preset_manager.presets[:5]
            return [
                RecommendationResult(
                    preset=p,
                    score=0,
                    confidence=0.3,
                    match_reasons=["Default recommendation"],
                    tag_matches={},
                )
                for p in presets
            ]

        results: list[RecommendationResult] = []
        unique_tags = set(self.collected_tags)

        for preset in self.preset_manager.presets:
            score = 0.0
            match_reasons: list[str] = []
            tag_matches: dict[str, int] = {}

            preset_tag_set = set(t.lower() for t in preset.tags)

            for tag in unique_tags:
                tag_lower = tag.lower()

                if tag_lower in preset_tag_set:
                    weight = self.tag_weights.get(tag, 1.0)
                    score += QUIZ_SCORE_TAG_EXACT * weight
                    tag_matches[tag] = tag_matches.get(tag, 0) + 1
                    match_reasons.append(f"Matches tag: {tag}")

                for ptag in preset_tag_set:
                    if tag_lower in ptag or ptag in tag_lower:
                        if ptag != tag_lower:
                            weight = self.tag_weights.get(tag, 1.0)
                            score += QUIZ_SCORE_TAG_PARTIAL * weight
                            tag_matches[tag] = tag_matches.get(tag, 0) + 1

            if preset.category == "student" and "student" in unique_tags:
                score += QUIZ_SCORE_CATEGORY
                match_reasons.append("Student category match")
            if preset.category == "professional" and any(
                t in unique_tags for t in ["professional", "career"]
            ):
                score += QUIZ_SCORE_CATEGORY
                match_reasons.append("Professional category match")

            difficulty_tags = {"beginner", "intermediate", "advanced", "professional"}
            if preset.difficulty in unique_tags:
                score += QUIZ_SCORE_DIFFICULTY
                match_reasons.append(f"Difficulty level: {preset.difficulty}")

            language_tags = {"python", "javascript", "java", "cpp", "c", "rust", "go", "typescript"}
            preset_lang_tags = preset_tag_set & language_tags
            matched_lang = unique_tags & preset_lang_tags
            if matched_lang:
                score += QUIZ_SCORE_LANGUAGE
                match_reasons.append(f"Language match: {', '.join(list(matched_lang)[:2])}")

            if score > 0:
                score += QUIZ_SCORE_BASE
                max_possible_score = (
                    len(unique_tags) * 3.0 * max(self.tag_weights.values(), default=1.0)
                )
                confidence = (
                    min(score / max_possible_score * 2, 1.0) if max_possible_score > 0 else 0.3
                )

                results.append(
                    RecommendationResult(
                        preset=preset,
                        score=score,
                        confidence=confidence,
                        match_reasons=match_reasons[:3],
                        tag_matches=tag_matches,
                    )
                )

        results.sort(key=lambda x: (x.score, x.confidence), reverse=True)

        return results[:5]

    def display_recommendations(self, results: list[RecommendationResult]) -> None:
        """Display preset recommendations in a formatted table."""
        if not results:
            console.print("\n[yellow]No matching presets found.[/]")
            return

        console.print()
        console.print("[bold green]" + "═" * 50 + "[/]")
        console.print("[bold green]      Your Top Recommendations[/]")
        console.print("[bold green]" + "═" * 50 + "[/]")
        console.print()

        table = Table(show_header=True, header_style="bold cyan", show_lines=False)
        table.add_column("#", style="dim", width=3)
        table.add_column("Preset", width=25)
        table.add_column("Match", width=8, justify="center")
        table.add_column("Category", width=12)
        table.add_column("Difficulty", width=12)
        table.add_column("Extensions", justify="center", width=10)

        for i, result in enumerate(results[:5], 1):
            confidence_str = f"{result.confidence:.0%}"
            diff_color = DIFFICULTY_COLORS.get(result.preset.difficulty, "white")
            table.add_row(
                str(i),
                truncate_string(result.preset.name, 23),
                f"[green]{confidence_str}[/]"
                if result.confidence > 0.6
                else f"[yellow]{confidence_str}[/]",
                result.preset.category.title(),
                f"[{diff_color}]{result.preset.difficulty.title()}[/]",
                str(result.preset.extension_count),
            )

        console.print(table)
        console.print()

        console.print("[bold]Top Pick Details:[/]")
        console.print()

        for i, result in enumerate(results[:3], 1):
            panel = self._create_recommendation_panel(result, i)
            console.print(panel)
            console.print()

    def _create_recommendation_panel(self, result: RecommendationResult, rank: int) -> Panel:
        """Create a Rich panel for a recommendation."""
        text = Text()

        name_style = "bold cyan"
        if rank == 1:
            name_style = "bold yellow"
        elif rank == 2:
            name_style = "bold white"

        text.append(f"{result.preset.name}\n", style=name_style)
        text.append(f"{result.preset.description}\n\n", style="dim")

        text.append("Why this preset:\n", style="italic")
        for reason in result.match_reasons[:3]:
            text.append(f"  • {reason}\n", style="green")

        text.append(f"\nTags: ", style="dim")
        text.append(", ".join(result.preset.tags[:5]), style="white")

        return Panel(
            text,
            title=f"[bold]#{rank}[/] {result.confidence:.0%} Match",
            border_style="cyan" if rank == 1 else "blue",
            padding=(1, 2),
        )

    def get_recommendation_by_quick_tags(
        self, tags: list[str], limit: int = 5
    ) -> list[RecommendationResult]:
        """Get quick recommendations based on tags without running quiz."""
        self.collected_tags = tags
        self.tag_weights = {tag: 1.0 for tag in tags}
        return self._calculate_recommendations()[:limit]


class QuickQuiz:
    """Simplified quick recommendation based on keywords."""

    KEYWORD_MAP: dict[str, list[str]] = {
        "python beginner": ["python", "student", "beginner"],
        "python": ["python"],
        "python data": ["python", "data", "pandas"],
        "python ml": ["python", "ml", "data"],
        "web dev": ["javascript", "typescript", "react", "vue", "frontend"],
        "web development": ["javascript", "typescript", "react", "vue", "frontend"],
        "frontend": ["javascript", "typescript", "react", "vue", "frontend"],
        "frontend react": ["javascript", "typescript", "react"],
        "frontend vue": ["javascript", "typescript", "vue"],
        "backend": ["nodejs", "go", "golang", "backend"],
        "nodejs": ["nodejs", "javascript", "backend"],
        "fullstack": ["fullstack", "nodejs", "javascript", "typescript"],
        "data": ["data", "pandas", "jupyter", "ml"],
        "data science": ["data", "pandas", "jupyter", "ml"],
        "ml": ["data", "pandas", "jupyter", "ml"],
        "machine learning": ["data", "pandas", "jupyter", "ml"],
        "competitive": ["competitive", "dsa", "algorithms", "cpp"],
        "competitive programming": ["competitive", "dsa", "algorithms", "cpp"],
        "dsa": ["competitive", "dsa", "algorithms"],
        "algorithms": ["competitive", "dsa", "algorithms"],
        "java": ["java"],
        "java spring": ["java", "spring"],
        "rust": ["rust"],
        "go": ["go", "golang"],
        "golang": ["go", "golang"],
        "c cpp": ["cpp", "c", "systems"],
        "c++": ["cpp", "c", "systems"],
        "systems": ["systems", "cpp", "rust"],
        "embedded": ["systems", "embedded", "cpp"],
        "mobile": ["mobile", "flutter"],
        "flutter": ["mobile", "flutter"],
        "android": ["mobile", "android"],
        "ios": ["mobile", "ios"],
        "devops": ["devops", "docker", "kubernetes"],
        "docker": ["devops", "docker", "kubernetes"],
        "kubernetes": ["devops", "docker", "kubernetes"],
        "cloud": ["devops", "cloud", "docker"],
        "aws": ["devops", "cloud", "aws"],
        "azure": ["devops", "cloud", "azure"],
        "remote": ["remote", "ssh"],
        "ssh": ["remote", "ssh"],
        "server": ["remote", "ssh", "server"],
        "student": ["student", "beginner"],
        "beginner": ["student", "beginner"],
        "minimal": ["minimal", "zen", "writing"],
        "writing": ["writing", "markdown", "documentation"],
        "markdown": ["writing", "markdown", "documentation"],
        "streaming": ["streaming", "youtube", "content"],
        "youtube": ["streaming", "youtube", "content"],
        "content creator": ["streaming", "youtube", "content"],
    }

    PRIORITY_KEYWORDS: list[str] = [
        "python beginner",
        "python ml",
        "python data",
        "frontend react",
        "frontend vue",
        "competitive programming",
        "machine learning",
        "fullstack",
    ]

    def __init__(self, preset_manager: PresetManager | None = None):
        """Initialize quick quiz."""
        self._preset_manager = preset_manager

    @property
    def preset_manager(self) -> PresetManager:
        """Get preset manager with lazy loading."""
        if self._preset_manager is None:
            self._preset_manager = get_preset_manager()
        return self._preset_manager

    def find_match(self, query: str) -> list[Preset]:
        """Find presets matching a query string."""
        query_lower = query.lower().strip()

        tags = self._extract_tags(query_lower)

        if not tags:
            return self.preset_manager.search_presets(query)

        recommendations = self.preset_manager.get_recommendations(list(set(tags)))
        return recommendations[:5]

    def _extract_tags(self, query: str) -> list[str]:
        """Extract matching tags from query."""
        tags: list[str] = []

        for keyword, mapped_tags in self.KEYWORD_MAP.items():
            if keyword in query:
                tags.extend(mapped_tags)

        return list(set(tags))

    def get_suggestions(self) -> list[tuple[str, str]]:
        """Get common query suggestions."""
        return [
            ("python beginner", "Start learning Python"),
            ("web dev", "Build websites"),
            ("data science", "Analyze data with Python"),
            ("competitive", "Practice coding algorithms"),
            ("devops", "Work with containers"),
            ("minimal", "Clean, distraction-free coding"),
        ]
