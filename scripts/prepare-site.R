# Run from the lesson root before building locally or deploying with Sandpaper.
# pkgdown supports lesson-local templates in site/pkgdown/templates/. Extend the
# installed Varnish head so every page, including generated reference pages,
# receives the same navigation styling without copying or editing theme assets.
# Retire this adapter when Sandpaper supports native sidebar groups.
theme_head <- system.file("pkgdown/templates/head.html", package = "varnish")
stopifnot(nzchar(theme_head))
navigation_css <- readLines("styles/workshop-navigation.css", warn = FALSE)
template_dir <- file.path("site", "pkgdown", "templates")
dir.create(template_dir, recursive = TRUE, showWarnings = FALSE)
writeLines(
  c(readLines(theme_head, warn = FALSE),
    '<style id="workshop-navigation">', navigation_css, "</style>"),
  file.path(template_dir, "head.html")
)

# Sandpaper 0.20.2 can reuse the instructor-notes HTML despite a changed local
# template. Invalidate those two generated pages so they receive the new head.
# Remove this invalidation when Sandpaper tracks local template changes there.
notes_cache <- file.path("site", "docs", c("instructor-notes.html",
                                         "instructor/instructor-notes.html"))
unlink(notes_cache)
