// webpack4的配置
module.exports = {
    // webpack4需要添加这个配置，development为开发环境，production为生产环境
    mode: "development",
    entry: __dirname + "/MelodieInfra/core/main.js", // 之前提到的唯一入口文件
    output: {
        path: __dirname + "/common", // 打包后的文件存放的地方
        filename: "index.js" // 打包后输出文件的文件名
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
}