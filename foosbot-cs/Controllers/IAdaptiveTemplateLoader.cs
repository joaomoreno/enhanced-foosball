// <copyright file="IAdaptiveTemplateLoader.cs" company="Microsoft">
// Copyright (c) Microsoft. All rights reserved.
// </copyright>
namespace Microsoft.BotBuilderSamples.Controllers
{
    using Microsoft.Bot.Schema;

    public interface IAdaptiveTemplateLoader
    {

        // TODO: we don't need this one once we have the generic Enum -> Attachment method
        string InitializeAdaptiveTemplate(string templateName);
    }
}