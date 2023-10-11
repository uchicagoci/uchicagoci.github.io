# Instructions

## To run locally (not on GitHub Pages, to serve on your own computer)

1. Clone the repository and made updates as necessary
1. Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
1. Run `bundle clean` to clean up the directory (no need to run `--force`)
1. Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.
1. Run `bundle exec jekyll serve -l` to generate the HTML and serve it from `localhost:4000` the local server will automatically rebuild and refresh the pages on change.

## To publish (on GitHub Pagees)

1. Commit and push the changes to the `main` branch
2. Run `./publish.sh` to publish the changes to the `gh-pages` branch (TODO)

# Development

## Original repository
* [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/)
* [Academic Pages](https://github.com/academicpages/academicpages.github.io)

## Debugging notes

(10/11/23) ERROR NoMethodError: undefined method key? for nil:NilClass
* [This post](https://github.com/academicpages/academicpages.github.io/issues/943) suggests downgrading to 3.9.0, but it doesn’t work because github pages now depend on jekyll 3.9.3
* [This post](https://github.com/jekyll/jekyll/issues/9451) provides a simple solution: use `jekyll serve -l` instead of `jekyll livestream`