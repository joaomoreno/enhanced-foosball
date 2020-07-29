// <copyright file="BaseAdaptiveTemplateLoader.cs" company="Microsoft">
// Copyright (c) Microsoft. All rights reserved.
// </copyright>

namespace Microsoft.BotBuilderSamples.Controllers
{
    using System.IO;
    using Microsoft.Bot.Schema;

    public class BaseAdaptiveTemplateLoader : IAdaptiveTemplateLoader
    {
        private readonly string resourceRoot;

        public BaseAdaptiveTemplateLoader(string resourceRoot)
        {
            this.resourceRoot = resourceRoot;
        }

        public string InitializeAdaptiveTemplate(string templateName)
        {
            using (var resource = typeof(BaseAdaptiveTemplateLoader).Assembly.GetManifestResourceStream($"{this.resourceRoot}.AdaptiveCardTemplates.{templateName}"))
            {
                using (var templateReader = new StreamReader(resource))
                {
                    return templateReader.ReadToEnd();
                }
            }
        }
    }
}