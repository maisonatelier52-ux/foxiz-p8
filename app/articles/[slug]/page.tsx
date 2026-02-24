import React from 'react';
import Header from '@/app/components/layout/Header';
import Footer from '@/app/components/layout/Footer';
import articlesIndex from '@/public/data/all-articles-index.json';
import Link from 'next/link';
import { Metadata } from 'next';
import fs from 'fs/promises';
import path from 'path';

interface ArticlePageProps {
    params: {
        slug: string;
    };
}

export async function generateMetadata({ params }: ArticlePageProps): Promise<Metadata> {
    const { slug } = await (params as any);
    const article = articlesIndex.find(a => a.slug === slug);
    return {
        title: article ? `${article.title} | Nexus News` : 'Article | Nexus News',
        description: article?.shortdescription,
    };
}

async function getArticleData(slug: string) {
    try {
        const filePath = path.join(process.cwd(), 'public', 'data', 'articles', `${slug}.json`);
        const content = await fs.readFile(filePath, 'utf-8');
        return JSON.parse(content);
    } catch (err) {
        return null;
    }
}

export default async function ArticlePage({ params }: ArticlePageProps) {
    const { slug } = await (params as any);
    const article = await getArticleData(slug);
    const indexInfo = articlesIndex.find(a => a.slug === slug);

    if (!article) {
        if (!indexInfo) return <div>Article not found</div>;
        return (
            <main className="min-h-screen flex flex-col">
                <Header />
                <div className="flex-grow flex items-center justify-center">
                    <p className="text-xl text-muted">Article content is being updated. Please check back soon.</p>
                </div>
                <Footer />
            </main>
        );
    }

    return (
        <main className="min-h-screen flex flex-col">
            <Header />

            <article className="flex-grow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <header className="mb-12 text-center">
                    <Link href={`/category/${article.category.toLowerCase()}`} className="inline-block px-4 py-1.5 bg-primary/10 text-primary text-xs font-black uppercase tracking-widest rounded-full mb-8">
                        {article.category}
                    </Link>
                    <h1 className="font-serif text-4xl md:text-6xl font-black leading-tight mb-8">
                        {article.title}
                    </h1>
                    <p className="text-xl md:text-2xl text-muted font-light leading-relaxed mb-12 italic">
                        {indexInfo?.shortdescription}
                    </p>
                    <div className="flex items-center justify-center gap-6 text-sm border-y border-border py-6">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full overflow-hidden">
                                <img src={article.author.image || '/images/news/markets-1.webp'} alt={article.author.name} className="w-full h-full object-cover" />
                            </div>
                            <span className="font-bold">{article.author.name}</span>
                        </div>
                        <span className="text-muted opacity-30">|</span>
                        <span className="text-muted uppercase tracking-widest font-bold text-xs">{article.date}</span>
                    </div>
                </header>

                <div className="relative aspect-[21/9] rounded-3xl overflow-hidden mb-16 shadow-2xl">
                    <img
                        src={article.image || '/images/news/markets-1.webp'}
                        alt={article.title}
                        className="absolute inset-0 w-full h-full object-cover"
                    />
                </div>

                <div className="prose prose-xl prose-slate max-w-none font-sans leading-loose text-foreground/90">
                    {article.content.map((block: any, idx: number) => {
                        if (block.type === 'intro' || block.type === 'paragraph') {
                            return (
                                <p key={idx} className={`${block.hasDropCap ? 'text-2xl font-serif mb-8 first-letter:text-7xl first-letter:font-black first-letter:mr-3 first-letter:float-left first-letter:text-primary mb-8' : 'mb-8'}`}>
                                    {block.text}
                                </p>
                            );
                        }
                        if (block.type === 'heading') {
                            return <h2 key={idx} className="font-serif text-3xl font-black mt-16 mb-8 underline decoration-primary/30 decoration-8 underline-offset-4">{block.text}</h2>;
                        }
                        if (block.type === 'quote') {
                            return (
                                <blockquote key={idx} className="border-l-4 border-primary pl-8 my-12 italic text-3xl font-serif text-muted">
                                    "{block.text}"
                                </blockquote>
                            );
                        }
                        return null;
                    })}
                </div>
            </article>

            <Footer />
        </main>
    );
}
