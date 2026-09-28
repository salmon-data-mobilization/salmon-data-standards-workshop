# Contributing to Salmon Data Standards Workshop

Thank you for your interest in contributing to the Salmon Data Standards Workshop! We appreciate your time and effort in helping improve this project. This guide provides multiple ways to contribute, whether you're new to Git/GitHub or an experienced developer.

---

## General Guidelines

1. **Be Respectful**: We are committed to maintaining a welcoming and inclusive environment. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) and adhere to it while contributing.

2. **Start with Issues**: If you're unsure about a change or want to discuss an idea first, we encourage you to open a [GitHub Issue](https://github.com/salmon-data-mobilization/salmon-data-standards-workshop/issues) to start a conversation.

3. **Small Changes Welcome**: Even small contributions like fixing typos, improving clarity, or updating examples are incredibly valuable.

---

## Ways to Contribute

### 🐛 Report Issues

- Found a typo or unclear instruction? Open an issue!
- Encountered a problem with the workshop materials? Let us know!
- Have an idea for improvement? We'd love to hear it!

### ✏️ Edit Content

- Fix typos and improve clarity
- Update examples and exercises
- Add new content or improve existing lessons
- Translate content to other languages

### 🧪 Test Materials

- Try out the workshop exercises
- Test on different operating systems
- Verify that examples work as expected

---

## How to Contribute

We provide multiple pathways for contributing based on your comfort level with Git and GitHub:

### 🌟 Option A: Quick Edits via GitHub Web Interface

This is the easiest way to contribute if you're new to Git/GitHub or just want to make a quick fix.

#### For Episode Files (R Markdown files in the `episodes/` folder):

1. **Navigate to the file** you want to edit:

   - Go to the [episodes folder](https://github.com/salmon-data-mobilization/salmon-data-standards-workshop/tree/main/episodes)
   - Click on the file you want to edit (e.g., `introduction.Rmd`, `session-1.Rmd`)

2. **Edit the file**:

   - Click the **pencil icon** (✏️) in the top-right corner of the file view
   - Make your changes directly in the web editor
   - You can preview your changes using the "Preview" tab

3. **Propose your changes**:

   - Scroll down to the "Commit changes" section
   - Add a brief description of what you changed (e.g., "Fix typo in introduction")
   - Click **"Propose changes"**

4. **Create a Pull Request**:
   - GitHub will automatically create a pull request for you
   - Add a more detailed description if needed
   - Click **"Create pull request"**

#### For Other Files:

The same process works for any file in the repository - just navigate to the file and click the edit button.

### 🚀 Option B: Fork and Pull Request (For More Advanced Users)

If you're comfortable with Git and want to make multiple changes or work locally to build and preview the website:

#### Prerequisites:

- Git installed on your computer
- A GitHub account
- R and R Studio Installed on your computer

#### Building and Previewing the Website Locally:

Before making changes, you may want to build and preview the website locally to see how your changes will look:

1. **Install required R packages**:

   ```bash
   # Install sandpaper and varnish from GitHub
   Rscript -e "if (!require('remotes', quietly = TRUE)) install.packages('remotes'); remotes::install_github('carpentries/sandpaper'); remotes::install_github('carpentries/varnish')"
   ```

2. **Install pandoc** (required for building):

   ```bash
   # On macOS with Homebrew
   brew install pandoc

   # On Ubuntu/Debian
   sudo apt install pandoc

   # On Windows, download from https://pandoc.org/installing.html
   ```

3. **Build the website**:

   ```bash
   cd salmon-data-standards-workshop
   Rscript -e "sandpaper::build_lesson()"
   ```

4. **Preview the website**:

   ```bash
   Rscript -e "sandpaper::serve()"
   ```

   Then open your web browser and go to `http://localhost:4321`.

   The website will automatically refresh when you make changes to your source files.

5. **Stop the preview server**:
   - Press `Ctrl+C` in the terminal where the server is running

#### Steps:

1. **Fork the repository**:

   - Go to the [main repository](https://github.com/salmon-data-mobilization/salmon-data-standards-workshop)
   - Click the "Fork" button in the top-right corner
   - This creates your own copy of the repository

2. **Clone your fork locally**:

   ```bash
   git clone https://github.com/YOUR-USERNAME/salmon-data-standards-workshop.git
   cd salmon-data-standards-workshop
   ```

3. **Create a new branch**:

   ```bash
   git checkout -b your-feature-name
   ```

4. **Make your changes**:

   - Edit files using your preferred editor
   - For R Markdown files, you can use RStudio, VS Code, or any text editor
   - Test your changes if possible

5. **Commit your changes**:

   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

6. **Push to your fork**:

   ```bash
   git push origin your-feature-name
   ```

7. **Create a Pull Request**:
   - Go to your fork on GitHub
   - Click "Compare & pull request"
   - Add a description of your changes
   - Submit the pull request

### 📝 Option C: Using GitHub Issues

Issues are perfect for:

- Reporting bugs or problems
- Suggesting new features or improvements
- Asking questions about the content
- Discussing changes before implementing them

#### To create an issue:

1. Go to the [Issues tab](https://github.com/salmon-data-mobiliszation/salmon-data-standards-workshop/issues)
2. Click "New issue"
3. Choose the appropriate template (Bug report, Feature request, etc.)
4. Fill out the details and submit

---

## Content Guidelines

### R Markdown Files

- Use clear, concise language
- Include code examples that actually work
- Add comments to explain complex concepts
- Test your code chunks before submitting

### General Writing

- Write in clear, accessible language
- Use active voice when possible
- Include examples and analogies to help understanding
- Be inclusive and welcoming in tone

### File Organization

- Keep related content together
- Use descriptive file names
- Follow the existing structure and naming conventions

---

## Review Process

Every pull request should include a **Review preview** section with a public
Netlify link, the previewed commit, and the pages to review. A maintainer builds,
publishes and verifies the preview before inviting collaborators to review, and
refreshes it after changes. Contributors using GitHub's web editor can leave the
preview pending for a maintainer. Follow the
[shared review preview workflow](docs/entrypoints.md#shared-review-previews).

1. **Automated Checks**: All pull requests are automatically checked for basic issues
2. **Community Review**: Maintainers and community members review changes
3. **Feedback**: We may request changes or ask questions
4. **Merge**: Once approved, your changes will be merged into the main repository

---

## Getting Help

If you need help with any of these processes:

- Open an [issue](https://github.com/salmon-data-mobilization/salmon-data-standards-workshop/issues) with your question
- Check out [GitHub's documentation](https://docs.github.com/en/get-started) for Git/GitHub basics
- Join our community discussions

---

## Recognition

Contributors are recognized in:

- The project's README
- Release notes
- Community acknowledgments

Your contributions, no matter how small, make a big difference. Thank you for helping improve the Salmon Data Standards Workshop!
