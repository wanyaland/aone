require 'singularitygs'
require 'compass/import-once/activate'
require 'support-for'
require 'normalize-scss'

# Require any additional compass plugins here.


project_path = File.expand_path('.')

# Set this to the root of your project when deployed:
http_path = "/"
http_images_dir = "images"
css_dir = "stylesheets"
sass_dir = "sass"
images_dir = "images"
generated_images_dir = "images"
sprite_load_path = "source-images"
javascripts_dir = "javascripts"
sass_options = {
  :debug_info => false
}
sourcemap = true

# You can select your preferred output style here (can be overridden via the command line):
# output_style = :expanded or :nested or :compact or :compressed
output_style = :expanded
environment = :development

# To enable relative paths to assets via compass helper functions. Uncomment:
relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
line_comments = false


# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass sass scss && rm -rf sass && mv scss sass
