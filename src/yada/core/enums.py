from enum import Enum


class ProgrammingLanguage(str, Enum):
    # General Purpose / Popular Languages
    PYTHON = "Python"
    JAVA = "Java"
    CPP = "C++"
    C = "C"
    CSHARP = "C#"
    GO = "Go"
    RUST = "Rust"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    RUBY = "Ruby"
    PHP = "PHP"
    R = "R"
    MATLAB = "MATLAB"
    SCALA = "Scala"
    DART = "Dart"
    LUA = "Lua"
    PERL = "Perl"
    HASKELL = "Haskell"
    ELIXIR = "Elixir"
    CLOJURE = "Clojure"
    ERLANG = "Erlang"
    GROOVY = "Groovy"
    FSHARP = "F#"
    OCAML = "OCaml"
    FORTRAN = "Fortran"
    COBOL = "COBOL"
    ADA = "Ada"
    JULIA = "Julia"
    ZIG = "Zig"
    NIM = "Nim"
    V_LANG = "V"
    CRYSTAL = "Crystal"
    RACKET = "Racket"

    # Web/Frontend
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"
    HTML = "HTML"
    CSS = "CSS"
    SASS = "Sass/SCSS"
    LESS = "Less"
    JSX = "JSX"
    TSX = "TSX"
    VUE = "Vue"
    SVELTE = "Svelte"

    # Databases & Query Languages
    SQL = "SQL"
    PLSQL = "PL/SQL"
    TSQL = "T-SQL"
    MYSQL = "MySQL"
    PGSQL = "PostgreSQL"

    # Shell & Scripting
    BASH = "Bash"
    ZSH = "Zsh"
    FISH = "Fish"
    POWERSHELL = "PowerShell"
    BATCH = "Batch"
    VBSCRIPT = "VBScript"


class ConfigFile(str, Enum):
    """CONFIGURATION & DATA FILES ENUM"""

    JSON = "JSON"
    YAML = "YAML"
    TOML = "TOML"
    XML = "XML"
    INI = "INI"
    CONF = "Conf"
    CFG = "Cfg"
    PROPERTIES = "Properties"
    ENV = "Environment Variables"
    DOTENV = ".env"

    # Build & Package Managers
    MAKEFILE = "Makefile"
    CMAKE = "CMake"
    DOCKERFILE = "Dockerfile"
    DOCKERCOMPOSE = "Docker Compose"
    PKGBUILD = "PKGBUILD"

    # Package Lock Files
    PACKAGE_LOCK = "Package Lock"
    YARN_LOCK = "Yarn Lock"
    PNPM_LOCK = "pnpm Lock"
    COMPOSER_LOCK = "Composer Lock"
    GEMFILE_LOCK = "Gemfile Lock"
    CARGO_LOCK = "Cargo Lock"
    POETRY_LOCK = "Poetry Lock"
    PIPFILE_LOCK = "Pipfile Lock"
    UV_LOCK = "uv Lock"
    MIX_LOCK = "Mix Lock"

    # Version Control
    GIT = "Git"
    GITIGNORE = "Gitignore"
    GITATTRIBUTES = "Gitattributes"
    GITMODULES = "Gitmodules"
    GITCONFIG = "Git Config"
    GITBLAME = "Git Blame"
    SVN = "Subversion"
    HG = "Mercurial"

    # CI/CD
    GITHUB_ACTIONS = "GitHub Actions"
    GITLAB_CI = "GitLab CI"
    CIRCLE_CI = "Circle CI"
    JENKINS = "Jenkins"
    TRAVIS_CI = "Travis CI"
    AZURE_PIPELINES = "Azure Pipelines"
    BUILDKITE = "Buildkite"
    DRONE = "Drone CI"
    TEAMCITY = "TeamCity"

    # Container & Orchestration
    HELM = "Helm"
    KUBERNETES = "Kubernetes"
    TERRAFORM = "Terraform"
    ANSIBLE = "Ansible"
    PULUMI = "Pulumi"


class DocFile(str, Enum):
    """DOCUMENTATION & MARKUP FILES ENUM"""

    MARKDOWN = "Markdown"
    RST = "reStructuredText"
    TEX = "LaTeX"
    ADOC = "AsciiDoc"
    ORG = "Org Mode"
    MDX = "MDX"
    TYPORA = "Typora"

    # Documentation Generators
    JSDOC = "JSDoc"
    TSDOC = "TSDoc"
    PYDOC = "Python Docstring"
    JAVADOC = "JavaDoc"
    DOXYGEN = "Doxygen"
    ROOK = "Rook"

    # Plain Text
    TXT = "Plain Text"
    LOG = "Log File"
    LICENSE = "License"
    README = "README"
    CONTRIBUTING = "Contributing Guide"
    CHANGELOG = "Changelog"
    TODO = "TODO"


class OtherCodeFile(str, Enum):
    """OTHER CODE FILES ENUM"""

    GRAPHQL = "GraphQL"
    PROTOBUF = "Protocol Buffers"
    THRIFT = "Thrift"
    AVRO = "Avro"
    JSON_SCHEMA = "JSON Schema"
    OPENAPI = "OpenAPI/Swagger"
    RAML = "RAML"

    # Template Engines
    JINJA = "Jinja"
    HANDLEBARS = "Handlebars"
    MUSTACHE = "Mustache"
    EJS = "EJS"
    PUG = "Pug"
    HAML = "Haml"
    SLIM = "Slim"
    ERB = "ERB (Ruby)"
    JSP = "JSP"
    ASPX = "ASPX"

    # Data Science
    JUPYTER = "Jupyter Notebook"
    RMD = "R Markdown"
    QMD = "Quarto Markdown"
    STAN = "Stan"

    # Assembly & Low-level
    ASM = "Assembly"
    NASM = "NASM"
    MASM = "MASM"
    LLVM = "LLVM IR"
    WASM = "WebAssembly"
    WAT = "WebAssembly Text"

    # GPU Programming
    CUDA = "CUDA"
    OPENCL = "OpenCL"
    METAL = "Metal"
    HLSL = "HLSL"
    GLSL = "GLSL"

    # Build & Task Runners
    ANT = "Apache Ant"
    MAVEN = "Maven"
    GRADLE = "Gradle"
    BAZEL = "Bazel"
    PANTS = "Pants"
    SBT = "SBT"
    GNU_MAKE = "GNU Make"
    NINJA = "Ninja"
    MESON = "Meson"

    # Web Configs
    HTACCESS = ".htaccess"
    NGNIX = "NGINX Config"
    APACHE = "Apache Config"
    TRAEFIK = "Traefik"
    CORS = "CORS Config"

    # Syntax & Linting
    ESLINT = "ESLint Config"
    PRETTIER = "Prettier Config"
    STYLELINT = "Stylelint"
    RUBOCOP = "RuboCop"
    PYLINT = "Pylint Config"
    FLAKE8 = "Flake8 Config"
    BLACK = "Black Config"

    # Module & Dependency Files
    REQUIREMENTS = "Requirements.txt"
    PACKAGE_JSON = "package.json"
    CARGO_TOML = "Cargo.toml"
    GO_MOD = "go.mod"
    GO_SUM = "go.sum"
    GEMFILE = "Gemfile"
    PIPFILE = "Pipfile"
    PYPROJECT = "pyproject.toml"
    SETUP_PY = "setup.py"
    SETUP_CFG = "setup.cfg"
    COMPOSER_JSON = "composer.json"
    PODSPEC = "Podspec"

    # IDE & Editor Configs
    VSCODE = "VS Code Config"
    EDITORCONFIG = "EditorConfig"
    VIM = "Vim Config"
    EMACS = "Emacs Config"
    ATOM = "Atom Config"
    SUBLIME = "Sublime Text Config"
    INTELLIJ = "IntelliJ Config"
    CLION = "CLion Config"

    # Tool Configs
    PYTEST = "Pytest Config"
    JEST = "Jest Config"
    MOCHA = "Mocha Config"
    KARMA = "Karma Config"
    CYPRESS = "Cypress Config"
    PLAYWRIGHT = "Playwright Config"
    SELENIUM = "Selenium Config"
    WEBPACK = "Webpack Config"
    VITE = "Vite Config"
    ROLLUP = "Rollup Config"
    ESBUILD = "esbuild Config"
    SNOWPACK = "Snowpack Config"
    PARCEL = "Parcel Config"

    # Database & Migration
    MIGRATION = "Database Migration"
    SEED = "Database Seed"
    SCHEMA = "Database Schema"
    PRISMA = "Prisma Schema"
    SEQUELIZE = "Sequelize"
    ALEMBIC = "Alembic"
    FLYWAY = "Flyway"
    LIQUIBASE = "Liquibase"
