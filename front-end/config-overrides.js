module.exports = {
  webpack: function(config, env) {
 
    return config;
  },
  jest: function(config) {
    // Here you can update Jest configurations
    config.transformIgnorePatterns = [
      "/node_modules/(?!(axios)/)"
    ];
    return config;
  }
}
