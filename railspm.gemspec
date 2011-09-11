# -*- encoding: utf-8 -*-
$:.push File.expand_path("../lib", __FILE__)
require "railspm/version"

Gem::Specification.new do |s|
  s.name        = "railspm"
  s.version     = Railspm::VERSION
  s.authors     = ["Tejas Dinkar"]
  s.email       = ["tejas@gja.in"]
  s.homepage    = ""
  s.summary     = %q{A gem to package rails app into an rpm(s)}
  s.description = %q{This should generate two rpms. This will have bundle deployed --production}

  s.rubyforge_project = "railspm"

  s.files         = `git ls-files`.split("\n")
  s.test_files    = `git ls-files -- {test,spec,features}/*`.split("\n")
  s.executables   = `git ls-files -- bin/*`.split("\n").map{ |f| File.basename(f) }
  s.require_paths = ["lib"]

  # specify any dependencies here; for example:
  # s.add_development_dependency "rspec"
  # s.add_runtime_dependency "rest-client"
end
