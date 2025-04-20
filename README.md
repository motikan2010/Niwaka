# Niwaka

## 準備

### 1 - 設定値の指定 （Slack トークンやOpenAI API キー など）

#### 1.1 - app/.env

`.env.example` をコピーして設定してください。

- **BOT_TOKEN** : Slack API の"OAuth Tokens"
- **APP_TOKEN** : Slack API の"App-Level Tokens"
- **CHANNEL_ID** : Slack のチャンネルID

#### 1.2 - .llm/config.json

`config.json.example` をコピーして設定してください。

- **OPENAI_API_KEY** : OpenAI API キー
- **REPO_NAME** : 検査対象リポジトリ（リポジトリは手動で clone する必要があります）
- **GITHUB_PERSONAL_ACCESS_TOKEN** : Github の Personal access tokens(アクセストークン)

### 2 - ソースコードの配置

　`repos`配下にAIが参照するソースコードのリポジトリを配置する。

## 起動

```
make up
 or 
docker compose up
```

