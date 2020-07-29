using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Security.Policy;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Connector;
using Microsoft.Bot.Connector.Authentication;
using Microsoft.Bot.Schema;
using Microsoft.Bot.Schema.Teams;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;

namespace Microsoft.BotBuilderSamples.Controllers
{
    [Route("api/game")]
    [ApiController]
    public class GameStart : ControllerBase
    {
        private readonly ConnectorClient client;
        private string _appId;
        private string _appPassword;
        private Dictionary<string, string> convos;
        private string gameStartTemplate;
        private string gameUpdateTemplate;

        public GameStart(IConfiguration configuration, IAdaptiveTemplateLoader loader, Dictionary<string, string> convos)
        {
            _appId = configuration["MicrosoftAppId"];
            _appPassword = configuration["MicrosoftAppPassword"];
            AppCredentials.TrustServiceUrl("https://smba.trafficmanager.net/amer/");
            this.client = new ConnectorClient(new Uri("https://smba.trafficmanager.net/amer/"), microsoftAppId: this._appId, microsoftAppPassword: this._appPassword);
            
            this.convos = convos;
            
            this.gameStartTemplate = loader.InitializeAdaptiveTemplate("MatchStart.json");
            this.gameUpdateTemplate = loader.InitializeAdaptiveTemplate("MatchUpdate.json");
        }

        [HttpPost]
        [Route("start")]
        public async Task<string> StartAsync([FromBody] MatchStartPayload payload)
        {
            //var cardJson = this.transformer.Transform(this.customerProfileTemplate, JsonConvert.SerializeObject(jsonData));
            var attachment = new Attachment
            {
                ContentType = "application/vnd.microsoft.card.adaptive",
                Content = JsonConvert.DeserializeObject(gameStartTemplate),
            };

            var conversationParameters = new ConversationParameters
            {
                IsGroup = true,
                ChannelData = new TeamsChannelData
                {
                    Channel = new ChannelInfo("19:a9b3ce0b5d1a4384bce8f32e96ea6c7a@thread.skype"),
                },
                Activity = (Activity)MessageFactory.Attachment(attachment)
            };

            var result = await client.Conversations.CreateConversationAsync(conversationParameters);
            convos[result.Id] = result.ActivityId;

            // Post follow up message
            var message = Activity.CreateMessageActivity();
            message.Text = payload.Message;
            await client.Conversations.ReplyToActivityAsync(result.Id, convos[result.Id], (Activity)message);

            // Return the thread id
            return await Task.FromResult(result.Id);
        }

        [HttpPost]
        [Route("update")]
        public async Task UpdateAsync([FromBody]MatchUpdatePayload updatePayload)
        {
            var attachment = new Attachment
            {
                ContentType = "application/vnd.microsoft.card.adaptive",
                Content = JsonConvert.DeserializeObject(gameUpdateTemplate),
            };

            //var message = Activity.CreateMessageActivity();
            //message.Text = updatePayload.Message;

            var convoId = updatePayload.ConversationId;
            await client.Conversations.ReplyToActivityAsync(convoId, convos[convoId], (Activity)MessageFactory.Attachment(attachment));
        }
    }

    public class MatchStartPayload
    {
        public string Title { get; set; }

        public string Score { get; set; }

        public string Message { get; set; }
    }

    public class MatchUpdatePayload : MatchStartPayload
    {
        public string ConversationId { get; set; }

        public string Replay { get; set; }
    }
}
